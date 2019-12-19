"""
Zachary Cook

Runs the program and creates the program XML fields.
"""

from Parser.XSDParser import XSDParser
from functools import cmp_to_key
import os
import re

XSD_DIRECTORY = "xsd/"



"""
Compares two schema file names.
"""
def compareSchemaNames(name1,name2):
    version1 = re.findall(r'\d+',name1)
    version2 = re.findall(r'\d+',name2)
    majorVersion1,minorVersion1 = int(version1[0]),int(version1[1])
    majorVersion2,minorVersion2 = int(version2[0]),int(version2[1])

    # Compare the versions.
    if majorVersion1 == majorVersion2:
        return minorVersion1 - minorVersion2
    else:
        return majorVersion1 - majorVersion2


if __name__ == '__main__':
    # Get the files to read and sort them.
    filesToRead = os.listdir(XSD_DIRECTORY)
    filesToRead = sorted(filesToRead,key=cmp_to_key(compareSchemaNames))

    # Parse the XSD objects.
    baseXSDs = []
    for fileName in filesToRead:
        print("Reading " + XSD_DIRECTORY + fileName)
        baseXSDs.append(XSDParser.createFromFile(XSD_DIRECTORY + fileName))