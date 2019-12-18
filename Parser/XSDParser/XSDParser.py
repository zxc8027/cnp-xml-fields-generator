"""
Zachary Cook

Parses XSD files.
"""

from xml.etree import ElementTree
from Parser.XSDParser import XSDData



XSD_PRIMITIVE_TYPES = [
    "int","integer","long","decimal",
    "string","base64Binary",
    "boolean",
    "dateTime","date",
]



"""
Removes the schema information from a string.
"""
def removeSchemaInformation(string):
    # Remove the schema if it exists.
    schemaEnd = string.find("}")
    if schemaEnd != -1:
        return string[schemaEnd + 1:]

    # Remove the pre-colon if it exists.
    schemaEnd = string.find(":")
    if schemaEnd != -1:
        return string[schemaEnd + 1:]

    # Return the base string.
    return string



"""
Class representing a parsed XSD.
"""
class XSD:
    """
    Creates an XSD object.
    """
    def __init__(self):
        self.namespace = None
        self.types = []
        self.elements = []

    """
    Adds a type.
    """
    def addType(self,xsdType):
        # Throw an exception if the type exists and can't be merged.
        existingType = self.getType(xsdType.name)

        if existingType is not None:
            if isinstance(existingType,XSDData.XSDSimpleType) and isinstance(xsdType,XSDData.XSDSimpleType):
                print("Type already exists; merging " + xsdType.name)

                # Merge the restrictions.
                for restrictionName in xsdType.restrictions.keys():
                    existingType.addRestriction(restrictionName,xsdType.restrictions[restrictionName])

                # Merge the enums.
                for enum in xsdType.enums:
                    if enum not in existingType.enums:
                        existingType.addEnumeration(enum)
            else:
                raise IndexError("Type already processed with name and can't be merged: " + xsdType.name)
        else:
            # Add the type.
            self.types.append(xsdType)

    """
    Adds an element.
    """
    def addElement(self,xsdElement):
        # Throw an exception if the type exists.
        if self.getElement(xsdElement.name):
            raise IndexError("Type already processed with name: " + xsdElement.name)

        # Add the type.
        self.elements.append(xsdElement)

    """
    Returns if a type is valid (is a base or links to another).
    Does not check for cyclic classes.
    """
    def isTypeValid(self,typeName):
        # Return true if it is a base type.
        if typeName is None or typeName in XSD_PRIMITIVE_TYPES:
            return True

        # Get the next type name and return false if it doesn't exists.
        nextType = self.getType(typeName)
        nextElement = self.getElement(typeName)
        if nextType is None and nextElement is None:
            return False

        # Return the next type.
        if nextType is not None:
            return self.isTypeValid(nextType.base)
        else:
            return self.isTypeValid(nextElement.base)

    """
    Returns an XSD type for the given name.
    """
    def getType(self,typeName):
        for xsdType in self.types:
            if xsdType.name.lower() == typeName.lower():
                return xsdType

    """
    Returns an XSD element for the given name.
    """
    def getElement(self,elementName):
        for xsdElement in self.elements:
            if xsdElement.name.lower() == elementName.lower():
                return xsdElement

    """
    Returns the element of a given tag, stopping at types.
    """
    def getChildElementOfName(self,element,expectedTagName):
        # Return a child if a child is valid.
        for child in element:
            tagName = removeSchemaInformation(child.tag)

            # Return if the tag name matches.
            if tagName == expectedTagName:
                return child

            # Check the children.
            if tagName != "complexType" and tagName != "simpleType":
                subElement = self.getChildElementOfName(child,expectedTagName)
                if subElement is not None:
                    return subElement

    """
    Processes a child element in a complex type.
    Returns the elements to add as a list.
    """
    def processComplexElementChild(self,element):
        elements = []

        # Get the tag name.
        tagName = removeSchemaInformation(element.tag)

        # Process the element.
        if tagName == "sequence" or tagName == "all" or tagName == "choice":
            # Create the group.
            group = XSDData.XSDGroup(tagName)
            elements.append(group)

            # Add the children.
            for child in element:
                for subChild in self.processComplexElementChild(child):
                    group.addItem(subChild)
        elif tagName == "attribute":
            # Get the attribute data.
            name = element.attrib["name"]
            type = removeSchemaInformation(element.attrib["type"])
            required = False
            default = None
            if "use" in element.attrib:
                if element.attrib["use"] == "required":
                    required = True
                elif element.attrib["use"] == "optional":
                    required = False
                else:
                    print("Unknown use attribute: " + element.attrib["use"])
            if "default" in element.attrib:
                default = element.attrib["default"]

            # Create and add the attribute.
            attribute = XSDData.XSDAttribute(name,type,required,default)
            elements.append(attribute)
        elif tagName == "element":
            # Get the element data.
            type = None
            minOccurrences = 0
            maxOccurrences = 1
            default = None
            if "ref" in element.attrib:
                name = removeSchemaInformation(element.attrib["ref"])
                type = name
            else:
                name = element.attrib["name"]
            if "minOccurs" in element.attrib:
                minOccurrences = int(element.attrib["minOccurs"])
            if "maxOccurs" in element.attrib:
                if element.attrib["maxOccurs"] == "unbounded":
                    maxOccurrences = (2 ** 31) - 1
                else:
                    maxOccurrences = int(element.attrib["maxOccurs"])
            if "default" in element.attrib:
                default = element.attrib["default"]

            # Get the type.
            if "type" in element.attrib:
                type = removeSchemaInformation(element.attrib["type"])
            elif len(element) == 1:
                typeElement = element[0]
                typeTagName = removeSchemaInformation(typeElement.tag)
                type = removeSchemaInformation(name)
                if typeTagName == "simpleType":
                    self.processSimpleType(typeElement,name)
                elif typeTagName == "complexType":
                    self.processComplexType(typeElement,name)
                else:
                    print("Unable to determine subtype of element: " + ElementTree.tostring(element,encoding="utf8",method="xml").decode("utf8"))
            elif type is None:
                print("Unable to determine type of element: " + ElementTree.tostring(element,encoding="utf8",method="xml").decode("utf8"))

            # Create and add the element.
            element = XSDData.XSDChildElement(name,type,default,minOccurrences,maxOccurrences)
            elements.append(element)
        elif tagName == "complexContent" or tagName == "extension" or tagName == "restriction":
            for child in element:
                for subChild in self.processComplexElementChild(child):
                    elements.append(subChild)
        else:
            print("Unable to process \"" + str(tagName) + "\": " + ElementTree.tostring(element,encoding="utf8",method="xml").decode("utf8"))

        # Return the elements.
        return elements

    """
    Processes a simple type.
    """
    def processSimpleType(self,element,name=None):
        # Parse a simple type (basic type with limits).
        restrictionElement = element[0]
        if "name" in element.attrib:
            name = removeSchemaInformation(element.attrib["name"])
        type = removeSchemaInformation(restrictionElement.attrib["base"])
        schemaObject = XSDData.XSDSimpleType(name,type)

        # Add the restrictions.
        for restriction in restrictionElement:
            restrictionName = removeSchemaInformation(restriction.tag)

            if restrictionName == "enumeration":
                schemaObject.addEnumeration(restriction.attrib["value"])
            else:
                schemaObject.addRestriction(restrictionName,restriction.attrib["value"])

        # Add the object.
        self.addType(schemaObject)

    """
    Processes a complex type.
    """
    def processComplexType(self,element,name,type=None):
        # Override the base type.
        extensionElement = self.getChildElementOfName(element,"extension")
        if extensionElement is not None:
            type = removeSchemaInformation(extensionElement.attrib["base"])
        else:
            extensionElement = self.getChildElementOfName(element,"restriction")
            if extensionElement is not None:
                type = removeSchemaInformation(extensionElement.attrib["base"])

        # Create the complex type.
        schemaObject = XSDData.XSDComplexType(name,type)

        # Process the child elements.
        for child in element:
            elementsToAdd = self.processComplexElementChild(child)
            for childItem in elementsToAdd:
                schemaObject.addItem(childItem)

        # Add the object.
        self.addType(schemaObject)

    """
    Populates the object from a string.
    """
    def fromString(self,xsdContents):
        # Parse the root schema element and get the schema.
        root = ElementTree.fromstring(xsdContents)
        self.namespace = root.attrib["targetNamespace"]

        # Read the child elements.
        for child in root:
            # Get the tag name.
            tagName = removeSchemaInformation(child.tag)

            # Parse the element.
            if tagName == "simpleType":
                self.processSimpleType(child)
            elif tagName == "element":
                name = removeSchemaInformation(child.attrib["name"])

                # Determine the base type.
                baseType = None
                if "substitutionGroup" in child.attrib:
                    baseType = removeSchemaInformation(child.attrib["substitutionGroup"])
                if "type" in child.attrib:
                    baseType = removeSchemaInformation(child.attrib["type"])

                # Add the element.
                self.addElement(XSDData.XSDComplexType(name,baseType))

                # Parse the complex type.
                if len(child) != 0:
                    firstChild = child[0]
                    firstChildTag = removeSchemaInformation(firstChild.tag)
                    if firstChildTag == "complexType":
                        self.processComplexType(firstChild,name,baseType)
                    else:
                        print("Unsupported child tag of " + str(name) + ": " + str(firstChildTag))
            elif tagName == "complexType":
                name = removeSchemaInformation(child.attrib["name"])
                self.processComplexType(child,name)
            else:
                print("Unsupported tag of " + str(tagName))



"""
Processes an XSD file to a set of schema objects.
"""
def processXSD(xsdContents):
    # Parse the XSD.
    xsd = XSD()
    xsd.fromString(xsdContents)

    # Return the XSD.
    return xsd

"""
"Flattens" an XSD object (removes all groups).
"""
def flattenXSD(existingXSD):
    # Create a new XSD.
    newXSD = XSD()
    newXSD.namespace = existingXSD.namespace

    # Flatten the types.
    for type in existingXSD.types:
        if isinstance(type,XSDData.XSDSimpleType):
            newXSD.addType(type)
        else:
            newXSD.addType(type.flatten())

    # Add the elements.
    for element in existingXSD.elements:
        newXSD.addElement(element)

    # Return the new XSD.
    return newXSD

"""
Validates that the types of a flatten XSD are valid.
"""
def validateXSDTypes(xsd):
    invalidXSDs = ""

    # Iterate through the types.
    for type in xsd.types:
        if not xsd.isTypeValid(type.base):
            invalidXSDs += "(Type) " + str(type.name) + " (Base is invalid)\n"

        if isinstance(type,XSDData.XSDComplexType):
            for item in type.childItems:
                if not xsd.isTypeValid(item.type):
                    invalidXSDs += "(Type) " + str(type.name) + "." + item.type + "\n"

    # Iterate through the elements.
    for element in xsd.elements:
        if not xsd.isTypeValid(element.base):
            invalidXSDs += "(Element) " + str(element.name) + "\n"

    # Raise an error if validation failed.
    if invalidXSDs != "":
        raise AttributeError("Missing inheritance references are detected in the following:\n\n" + invalidXSDs + "\nThis may be due to an incomplete list of primitives in the script, or incorrect inheritance references.")



if __name__ == '__main__':

    with open("../../xsd/SchemaCombined_v12.10.xsd") as file:
        contents = file.read()

    xsd = flattenXSD(processXSD(contents))
    validateXSDTypes(xsd)