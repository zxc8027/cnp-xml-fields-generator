"""
Zachary Cook

Classes for storing XML schema data.
"""

"""
Class representing a simple type.
"""
class XSDSimpleType:
    """
    Creates a simple XSD type.
    """
    def __init__(self,name,base):
        self.name = name
        self.base = base
        self.enums = []
        self.restrictions = {}

    """
    Adds a restriction.
    """
    def addRestriction(self,name,value):
        self.restrictions[name] = value

    """
    Adds an enumeration.
    """
    def addEnumeration(self,value):
        self.enums.append(value)

    """
    Returns if the type is an enum.
    """
    def isEnum(self):
        return len(self.enums) != 0

"""
Class representing a complex type or element.
"""
class XSDComplexType:
    """
    Creates and complex XSD type.
    """
    def __init__(self,name,base):
        self.name = name
        self.base = base
        self.childItems = []

    """
    Adds a child item.
    """
    def addItem(self,item):
        # Return if the item already exists.
        for type in self.childItems:
            if (isinstance(type,XSDAttribute) or isinstance(type,XSDChildElement)) and (isinstance(item,XSDAttribute) or isinstance(item,XSDChildElement)) and type.name == item.name:
                return

        # Add the item.
        self.childItems.append(item)

    """
    "Flattens" the complex type.
    """
    def flatten(self):
        # Create a new complex type.
        newComplexType = XSDComplexType(self.name,self.base)

        # Add the child items.
        for type in self.childItems:
            if isinstance(type,XSDGroup):
                for subType in type.getAllChildren():
                    newComplexType.addItem(subType)
            else:
                newComplexType.addItem(type)

        # Return the new complex type.
        return newComplexType

"""
Class representing a child element.
"""
class XSDChildElement:
    """
    Creates and complex XSD child element.
    """
    def __init__(self,name,type,default=None,minOccurrences=0,maxOccurrences=1):
        self.name = name
        self.type = type
        self.default = default
        self.minOccurrences = minOccurrences
        self.maxOccurrences = maxOccurrences

"""
Class representing an attribute.
"""
class XSDAttribute:
    """
    Creates and complex XSD attribute.
    """
    def __init__(self,name,type,required=False,default=None):
        self.name = name
        self.type = type
        self.required = required
        self.default = default

"""
Class representing a group.
"""
class XSDGroup:
    """
    Creates and complex XSD group.
    """
    def __init__(self,type):
        self.type = type
        self.childItems = []

    """
    Adds a child item.
    """
    def addItem(self,item):
        self.childItems.append(item)

    """
    Returns all the child attributes and elements.
    """
    def getAllChildren(self):
        # Create a list.
        children = []

        # Add the child items.
        for type in self.childItems:
            if isinstance(type, XSDGroup):
                for subType in type.getAllChildren():
                    children.append(subType)
            else:
                children.append(type)

        # Return the list.
        return children