"""
Zachary Cook

Processes the differences between XSDs.
"""


# Names of objects to merge.
from Parser.XSDParser import XSDData

NAMES_TO_MERGE = {
    "litleInternalRecurringRequestType": "cnpInternalRecurringRequestType",
    "litleRequest": "cnpRequest",
    "litleResponse": "cnpResponse",
    "litleOnlineRequest": "cnpOnlineRequest",
    "litleOnlineResponse": "cnpOnlineResponse",
}



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
    def __init__(self,type):
        self.names = []
        self.nameRefs = {}
        self.type = type

    """
    Adds a name for a version.
    """
    def addNameForVersion(self,name,version,type=None):
        versionTag = NameVersion(name,version,version,type)
        self.names.append(versionTag)
        self.nameRefs[version] = versionTag

    """
    Merges the names together.
    Assumes the versions are in order.
    """
    def mergeNameVersions(self,versions):
        # Return if there aren't names to merge.
        if len(self.names) <= 1:
            return

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
    def addChildNameForVersion(self,commonName,encodeName,base,version,type=None):
        # Create the child element if it doesn't exist.
        if commonName not in self.childItems.keys():
            self.childItems[commonName] = VersionedItem(base)

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
    Adds a simple type.
    """
    def addSimpleType(self,simpleType,version):
        if simpleType.isEnum():
            # Add the item if it doesn't exist.
            if simpleType.name not in self.enums.keys():
                self.enums[simpleType.name] = VersionedComposite(simpleType.base)

            # Add the name.
            item = self.enums[simpleType.name]
            item.addNameForVersion(simpleType.name,version)

            # Add the enums.
            for enum in simpleType.enums:
                item.addChildNameForVersion(enum,enum,simpleType.base,version)
        else:
            # Add the item if it doesn't exist.
            if simpleType.name not in self.simpleTypes.keys():
                self.simpleTypes[simpleType.name] = VersionedItem(simpleType.base)

            # Add the name.
            self.simpleTypes[simpleType.name].addNameForVersion(simpleType.name,version)

    """
    Adds a complex type.
    """
    def addComplexType(self,complexType,version):
        # Get the name to store.
        storeName = complexType.name
        if storeName in NAMES_TO_MERGE.keys():
            storeName = NAMES_TO_MERGE[storeName]

        # Add the item if it doesn't exist.
        if storeName not in self.complexTypes.keys():
            self.complexTypes[storeName] = VersionedComposite(complexType.base)

        # Add the name.
        item = self.complexTypes[storeName]
        item.addNameForVersion(complexType.name,version)

        # Add the enums.
        for child in complexType.childItems:
            if isinstance(child,XSDData.XSDChildElement):
                item.addChildNameForVersion(child.name,child.name,child.type,version,"Element")
            else:
                item.addChildNameForVersion(child.name,child.name,child.type,version,"Attribute")

    """
    Adds an element.
    """
    def addElement(self,element,version):
        pass

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