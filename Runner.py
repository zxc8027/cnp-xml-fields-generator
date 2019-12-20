"""
Zachary Cook

Runs the program and creates the program XML fields.
"""

from Parser.FieldWriter import LanguageFieldWriter
from Parser.XSDParser import XSDParser, XSDVersionDiffer
from functools import cmp_to_key
import os

XSD_DIRECTORY = "xsd/"







if __name__ == '__main__':
    # Get the files to read and sort them.
    filesToRead = os.listdir(XSD_DIRECTORY)
    filesToRead = sorted(filesToRead,key=cmp_to_key(XSDVersionDiffer.compareVersionNames))

    # Get the list of versions
    versions = []
    for fileName in filesToRead:
        majorVersion,minorVersion = XSDVersionDiffer.getVersionFromName(fileName)
        versions.append(str(majorVersion) + "." + str(minorVersion))

    # Parse the XSD objects.
    baseXSDs = []
    for fileName in filesToRead:
        print("Reading " + XSD_DIRECTORY + fileName)
        baseXSDs.append(XSDParser.createFromFile(XSD_DIRECTORY + fileName))

    # Merge the XSDs together.
    versionedXSD = XSDVersionDiffer.VersionedXSD()
    for i in range(0,len(versions)):
        i = len(versions) - 1 - i
        version = versions[i]
        xsd = baseXSDs[i]

        print("Merging version " + version)
        versionedXSD.populateFromXSD(xsd,version)

    # Merge the versions.
    versionedXSD.mergeNameVersions(versions)

    # Write the files.
    LanguageFieldWriter.writeFieldFiles(versionedXSD,versions)