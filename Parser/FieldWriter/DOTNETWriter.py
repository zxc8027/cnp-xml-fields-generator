"""
Zachary Cook

Writer for the C# / .NET SDK.
"""

from Parser.FieldWriter import FieldWriter



"""
Class representing a .NET writer.
"""
class DOTNETWriter(FieldWriter.FieldWriter):
    """
    Creates a .NET writer object.
    """
    def __init__(self, xsd,version,outputDirectory):
        super().__init__(xsd,version,outputDirectory)

    """
    Returns the display name of the writer.
    """
    def getDisplayName(self):
        return "C# (.NET)"

    """
    Returns the file name of the writer.
    """
    def getFileName(self):
        return "XmlFields.cs"

    """
    Returns the file contents as a string.
    """
    def getContents(self):
        return "test"