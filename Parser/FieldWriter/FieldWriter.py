"""
Zachary Cook

Base class for writing files.
"""

import os



"""
Class representing a writer.
"""
class FieldWriter:
    """
    Creates a writer object.
    """

    def __init__(self, xsd, version, outputDirectory):
        self.xsd = xsd
        self.versions = version
        self.outputDirectory = outputDirectory

    """
    Returns the display name of the writer.
    """

    def getDisplayName(self):
        return "ROOT"

    """
    Returns the file name of the writer.
    """

    def getFileName(self):
        return "ROOT.txt"

    """
    Returns the file contents as a string.
    """

    def getContents(self):
        return ""

    """
    Writes the file.
    """

    def write(self):
        # Get the contents and destination.
        contents = self.getContents()
        location = self.outputDirectory + self.getFileName()

        # Create the output directory if it doesn't exist.
        if not os.path.exists(self.outputDirectory):
            os.mkdir(self.outputDirectory)

        # Write the file.
        with open(location, "w") as file:
            file.write(contents)