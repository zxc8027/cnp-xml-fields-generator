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
        self.childItems.append(item)

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