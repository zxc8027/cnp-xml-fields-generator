"""
Zachary Cook

Processes the differences between XSDs.
"""

from Parser.XSDParser import XSDData
from functools import cmp_to_key
import re

# Names of objects to merge.
NAMES_TO_MERGE = {
    "litleRequest": "cnpRequest",
    "litleResponse": "cnpResponse",
    "litleOnlineRequest": "cnpOnlineRequest",
    "litleOnlineResponse": "cnpOnlineResponse",
}



"""
Transform a name if it should be changed.
"""
def transformName(name):
    # Set the name if it exists to merge.
    if name in NAMES_TO_MERGE.keys():
        name = NAMES_TO_MERGE[name]

    # Return the name.
    return name

"""
Returns the major version and minor
version for a given file name.
"""
def getVersionFromName(name):
    version = re.findall(r'\d+',name)
    return int(version[0]),int(version[1])

"""
Compares two version names.
"""
def compareVersionNames(name1,name2):
    majorVersion1,minorVersion1 = getVersionFromName(name1)
    majorVersion2,minorVersion2 = getVersionFromName(name2)

    # Compare the versions.
    if majorVersion1 == majorVersion2:
        return minorVersion1 - minorVersion2
    else:
        return majorVersion1 - majorVersion2

"""
Sorts two name versions.
"""
def sortNameVersions(version1,version2):
    return compareVersionNames(version1.start,version2.start)



"""
Class representing a name version.
"""
class NameVersion:
    """
    Creates a name version object.
    """
    def __init__(self,name,start,end,type=None):
        self.name = name
        self.start = start
        self.end = end
        self.type = type

"""
Class repenting a versioned item.
"""
class VersionedItem:
    """
    Creates a versioned item.
    """
    def __init__(self,type,default=None,minOccurences=None,maxOccurences=None):
        self.names = []
        self.nameRefs = {}
        self.type = type
        self.default = default
        self.minOccurences = minOccurences
        self.maxOccurences = maxOccurences

    """
    Adds a name for a version.
    """
    def addNameForVersion(self,name,version,type=None):
        # Return if the version exists.
        if version in self.nameRefs.keys():
            return

        # Add the version.
        versionTag = NameVersion(name,version,version,type)
        self.nameRefs[version] = versionTag
        self.names.append(versionTag)

    """
    Merges the names together.
    Assumes the versions are in order.
    """
    def mergeNameVersions(self,versions):
        # Return if there aren't names to merge.
        if len(self.names) <= 1:
            return

        # Sort the names.
        self.names = sorted(self.names,key=cmp_to_key(sortNameVersions))

        # Find the first version index:
        currentVersionTag = 0
        firstVersion = versions.index(self.names[0].start)

        # Go through the versions and merge consecutive ranges.
        for i in range(firstVersion + 1,len(versions)):
            currentNameVersion = self.names[currentVersionTag]
            currentVersion = versions[i]

            if currentVersion in self.nameRefs.keys():
                versionToMerge = self.names[currentVersionTag + 1]
                if currentNameVersion.end == versions[i - 1] and currentNameVersion.name == versionToMerge.name and currentNameVersion.type == versionToMerge.type:
                    currentNameVersion.end = versionToMerge.end
                    self.names.pop(currentVersionTag + 1)
                    self.nameRefs.pop(currentVersion)
                else:
                    currentVersionTag += 1

"""
Class representing a versioned composite.
"""
class VersionedComposite(VersionedItem):
    """
    Creates a versioned simple type.
    """
    def __init__(self,type):
        super().__init__(type)
        self.childItems = {}

    """
    Adds a name for a child item.
    """
    def addChildNameForVersion(self,commonName,encodeName,base,version,type=None,default=None,minOccurences=None,maxOccurences=None):
        # Create the child element if it doesn't exist.
        if commonName not in self.childItems.keys():
            self.childItems[commonName] = VersionedItem(base,default,minOccurences,maxOccurences)

        # Add the version.
        self.childItems[commonName].addNameForVersion(encodeName,version,type)

    """
    Merges the names together.
    Assumes the versions are in order.
    """
    def mergeNameVersions(self,versions):
        super().mergeNameVersions(versions)

        # Merge the child items.
        for child in self.childItems.values():
            child.mergeNameVersions(versions)

"""
Class for storing XSD objects.
"""
class VersionedXSD:
    """
    Creates a versioned XSD object.
    """
    def __init__(self):
        self.enums = {}
        self.simpleTypes = {}
        self.complexTypes = {}
        self.elements = {}

    """
    Returns the complex type that contains a child
    with the name.
    """
    def getComplexTypeWithChild(self,type,itemName):
        # Return none if the type is undefined.
        if type is None:
            return None

        # Get the type and return if it contains the child.
        complexType = self.complexTypes[type]
        if itemName in complexType.childItems.keys():
            return type

        # Return the base's result.
        return self.getComplexTypeWithChild(complexType.type,itemName)

    """
    Adds a simple type.
    """
    def addSimpleType(self,simpleType,version):
        if simpleType.isEnum():
            # Add the item if it doesn't exist.
            if simpleType.name not in self.enums.keys():
                self.enums[simpleType.name] = VersionedComposite(transformName(simpleType.base))

            # Add the name.
            item = self.enums[simpleType.name]
            item.addNameForVersion(simpleType.name,version)

            # Add the enums.
            for enum in simpleType.enums:
                item.addChildNameForVersion(enum,enum,transformName(simpleType.base),version)
        else:
            # Add the item if it doesn't exist.
            if simpleType.name not in self.simpleTypes.keys():
                self.simpleTypes[simpleType.name] = VersionedItem(transformName(simpleType.base))

            # Add the name.
            self.simpleTypes[simpleType.name].addNameForVersion(simpleType.name,version)

    """
    Adds a complex type.
    """
    def addComplexType(self,complexType,version):
        storeName = transformName(complexType.name)

        # Add the item if it doesn't exist.
        if storeName not in self.complexTypes.keys():
            self.complexTypes[storeName] = VersionedComposite(transformName(complexType.base))

        # Add the name.
        item = self.complexTypes[storeName]
        item.addNameForVersion(complexType.name,version)

        # Add the enums.
        for child in complexType.childItems:
            if isinstance(child,XSDData.XSDChildElement):
                item.addChildNameForVersion(child.name,child.name,transformName(child.type),version,"Element",child.default,child.minOccurrences,child.maxOccurrences)
            else:
                item.addChildNameForVersion(child.name,child.name,transformName(child.type),version,"Attribute",child.default)

    """
    Adds an element.
    """
    def addElement(self,element,version):
        storeName = transformName(element.name)

        # Add the item if it doesn't exist.
        if storeName not in self.elements.keys():
            self.elements[storeName] = VersionedComposite(transformName(element.base))

        # Add the name.
        item = self.elements[storeName]
        item.addNameForVersion(element.name,version)

    """
    Populates the object from an XSD object.
    """
    def populateFromXSD(self,xsd,version):
        # Add the types.
        for type in xsd.types:
            if isinstance(type,XSDData.XSDSimpleType):
                self.addSimpleType(type,version)
            else:
                self.addComplexType(type,version)

        # Add the elements.
        for element in xsd.elements:
            self.addElement(element,version)

    """
    Merges the names together.
    Assumes the versions are in order.
    """
    def mergeNameVersions(self,versions):
        # Remove the duplicate children of the complex types. Simple types, enums, and elements don't have this problem.
        for complexType in self.complexTypes.values():
            for childName in list(complexType.childItems.keys()):
                child = complexType.childItems[childName]
                parentWithChildName = self.getComplexTypeWithChild(complexType.type,childName)

                # Merge the parent element if it exists.
                if parentWithChildName is not None:
                    parent = self.complexTypes[parentWithChildName]
                    for name in child.names:
                        parent.addChildNameForVersion(childName,name.name,child.type,name.start,name.type,child.default)

                    del complexType.childItems[childName]

        # Merge the simple types.
        for simpleType in self.simpleTypes.values():
            simpleType.mergeNameVersions(versions)

        # Merge the enums.
        for enum in self.enums.values():
            enum.mergeNameVersions(versions)

        # Merge the complex types.
        for complexType in self.complexTypes.values():
            complexType.mergeNameVersions(versions)

        # Merge the elements.
        for element in self.elements.values():
            element.mergeNameVersions(versions)