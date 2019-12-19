"""
Zachary Cook

Runs the program and creates the program XML fields.
"""

from Parser.FieldWriter import LanguageFieldWriter
from Parser.XSDParser import XSDParser, XSDVersionDiffer
from functools import cmp_to_key
import os
import re

XSD_DIRECTORY = "xsd/"



"""
Returns the major version and minor
version for a given file name.
"""
def getVersionFromName(name):
    version = re.findall(r'\d+',name)
    return int(version[0]),int(version[1])

"""
Compares two schema file names.
"""
def compareSchemaNames(name1,name2):
    majorVersion1,minorVersion1 = getVersionFromName(name1)
    majorVersion2,minorVersion2 = getVersionFromName(name2)

    # Compare the versions.
    if majorVersion1 == majorVersion2:
        return minorVersion2 - minorVersion1
    else:
        return majorVersion2 - majorVersion1



if __name__ == '__main__':
    # Get the files to read and sort them.
    filesToRead = os.listdir(XSD_DIRECTORY)
    filesToRead = sorted(filesToRead,key=cmp_to_key(compareSchemaNames))

    # Get the list of versions
    versions = []
    for fileName in filesToRead:
        majorVersion,minorVersion = getVersionFromName(fileName)
        versions.append(str(majorVersion) + "." + str(minorVersion))

    # Parse the XSD objects.
    baseXSDs = []
    for fileName in filesToRead:
        print("Reading " + XSD_DIRECTORY + fileName)
        baseXSDs.append(XSDParser.createFromFile(XSD_DIRECTORY + fileName))

    # Merge the XSDs together.
    versionedXSD = XSDVersionDiffer.VersionedXSD()
    for i in range(0,len(versions)):
        version = versions[i]
        xsd = baseXSDs[i]

        print("Merging version " + version)
        versionedXSD.populateFromXSD(xsd,version)

    # Merge the versions.
    versionedXSD.mergeNameVersions(versions)

    # Write the files.
    LanguageFieldWriter.writeFieldFiles(versionedXSD,versions)