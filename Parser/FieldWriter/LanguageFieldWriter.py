"""
Zachary Cook

Writes field files for all supported languages.
"""

from Parser.FieldWriter import DOTNETWriter



FILE_OUTPUT_LOCATION = "output/"

SUPPORTED_LANGUAGES = [
    DOTNETWriter.DOTNETWriter,
]



"""
Writes the versioned XSD for all languages.
"""
def writeFieldFiles(xsd,versions):
    for writerClass in SUPPORTED_LANGUAGES:
        # Create the writer.
        writer = writerClass(xsd,versions,FILE_OUTPUT_LOCATION)

        # Write the field file.
        print("Writing XML fields for " + writer.getDisplayName())
        writer.write()