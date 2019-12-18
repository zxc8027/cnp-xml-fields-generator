"""
Zachary Cook

Processes the differences between XSDs.
"""


# Names of objects to merge.
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
    def __init__(self,name,start,end):
        self.name = name
        self.start = start
        self.end = end

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
    def addNameForVersion(self,name,version):
        versionTag = NameVersion(name,version,version)
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
                if currentNameVersion.end == versions[i - 1] and currentNameVersion.name == versionToMerge.name:
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
    def addChildNameForVersion(self,commonName,encodeName,type,version):
        # Create the child element if it doesn't exist.
        if commonName not in self.childItems.keys():
            self.childItems[commonName] = VersionedItem(type)

        # Add the version.
        self.childItems[commonName].addNameForVersion(encodeName,version)

    """
    Merges the names together.
    Assumes the versions are in order.
    """
    def mergeNameVersions(self,versions):
        super().mergeNameVersions(versions)

        # Merge the child items.
        for child in self.childItems.values():
            child.mergeNameVersions(versions)