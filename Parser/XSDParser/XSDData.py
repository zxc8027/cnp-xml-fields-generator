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
    def __init__(self, name, base):
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

"""
Class representing a attribute.
"""

"""
Class representing an all group (all of the options).
"""

"""
Class representing a sequence group (any of the options).
"""

"""
Class representing a choice group (limited amount of options).
"""