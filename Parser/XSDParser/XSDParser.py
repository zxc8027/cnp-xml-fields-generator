"""
Zachary Cook

Parses XSD files.
"""

from xml.etree import ElementTree
from Parser.XSDParser import XSDData

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

    """
    Adds a type.
    """
    def addType(self,xsdType):
        # Throw an exception if the type exists.
        if self.getType(xsdType.name):
            raise IndexError("Type already processed with name: " + xsdType)

        # Add the type.
        self.types.append(xsdType)

    """
    Returns an XSD type for the given name.
    """
    def getType(self,typeName):
        for xsdType in self.types:
            if xsdType.name.lower() == typeName.lower():
                return xsdType

    """
    Processes a simple type.
    """
    def processSimpleType(self,element):
        # Parse a simple type (basic type with limits).
        restrictionElement = element[0]
        name = removeSchemaInformation(element.attrib["name"])
        type = removeSchemaInformation(restrictionElement.attrib["base"])
        schemaObject = XSDData.XSDSimpleType(name, type)
        self.addType(schemaObject)

        # Add the restrictions.
        for restriction in restrictionElement:
            restrictionName = removeSchemaInformation(restriction.tag)

            if restrictionName == "enumeration":
                schemaObject.addEnumeration(restriction.attrib["value"])
            else:
                schemaObject.addRestriction(restrictionName, restriction.attrib["value"])
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
                firstChild = child[0]
                firstChildName = removeSchemaInformation(firstChild.attrib["name"])

                # Determine the base type.
                baseType = None
                if "substitutionGroup" in child.attrib:
                    baseType = child.attrib["substitutionGroup"]

"""
Processes an XSD file to a set of schmea objects.
"""
def processXSD(xsdContents):
    # Parse the XSD.
    xsd = XSD()
    xsd.fromString(xsdContents)

    # Return the XSD.
    return xsd


if __name__ == '__main__':

    with open("xsd/SchemaCombined_v12.10.xsd") as file:
        contents = file.read()

    processXSD(contents)