"""
Zachary Cook

Tests the XSD differ.
"""

import unittest
from Parser.XSDParser import XSDVersionDiffer, XSDData



class VersionedItemTests(unittest.TestCase):
    """
    Tests the mergeNameVersions method.
    """
    def testMergeNameVersions(self):
        # Create a versioned item and add names.
        item = XSDVersionDiffer.VersionedItem("type")
        item.addNameForVersion("TestName1","8.4")
        item.addNameForVersion("TestName1","8.5")
        item.addNameForVersion("TestName1","9.0")
        item.addNameForVersion("TestName1","9.1")
        item.addNameForVersion("TestName1","9.3")
        item.addNameForVersion("TestName1","9.4")
        item.addNameForVersion("TestName1","9.5")
        item.addNameForVersion("TestName1","9.6")
        item.addNameForVersion("TestName2","9.7")
        item.addNameForVersion("TestName1","9.8")

        # Merge the names and assert the merge was correct.
        item.mergeNameVersions(["8.0","8.1","8.2","8.3","8.4","8.5","9.0","9.1","9.2","9.3","9.4","9.5","9.6","9.7","9.8"])
        self.assertEqual(len(item.names),4)
        self.assertEqual(item.names[0].name,"TestName1")
        self.assertEqual(item.names[0].start,"8.4")
        self.assertEqual(item.names[0].end,"9.1")
        self.assertEqual(item.names[0].type,None)
        self.assertEqual(item.names[1].name,"TestName1")
        self.assertEqual(item.names[1].start,"9.3")
        self.assertEqual(item.names[1].end,"9.6")
        self.assertEqual(item.names[1].type,None)
        self.assertEqual(item.names[2].name,"TestName2")
        self.assertEqual(item.names[2].start,"9.7")
        self.assertEqual(item.names[2].end,"9.7")
        self.assertEqual(item.names[2].type,None)
        self.assertEqual(item.names[3].name,"TestName1")
        self.assertEqual(item.names[3].start,"9.8")
        self.assertEqual(item.names[3].end,"9.8")
        self.assertEqual(item.names[3].type,None)

    """
    Tests the mergeNameVersions method with types.
    """
    def testMergeNameVersionsTypes(self):
        # Create a versioned item and add names.
        item = XSDVersionDiffer.VersionedItem("type")
        item.addNameForVersion("TestName1","8.4","Element")
        item.addNameForVersion("TestName1","8.5","Element")
        item.addNameForVersion("TestName1","9.0","Attribute")
        item.addNameForVersion("TestName1","9.1","Element")
        item.addNameForVersion("TestName1","9.3","Element")
        item.addNameForVersion("TestName1","9.4","Element")
        item.addNameForVersion("TestName1","9.5","Element")
        item.addNameForVersion("TestName1","9.6","Element")
        item.addNameForVersion("TestName2","9.7","Element")
        item.addNameForVersion("TestName1","9.8","Element")

        # Merge the names and assert the merge was correct.
        item.mergeNameVersions(["8.0","8.1","8.2","8.3","8.4","8.5","9.0","9.1","9.2","9.3","9.4","9.5","9.6","9.7","9.8"])
        self.assertEqual(len(item.names),6)
        self.assertEqual(item.names[0].name,"TestName1")
        self.assertEqual(item.names[0].start,"8.4")
        self.assertEqual(item.names[0].end,"8.5")
        self.assertEqual(item.names[0].type,"Element")
        self.assertEqual(item.names[1].name,"TestName1")
        self.assertEqual(item.names[1].start,"9.0")
        self.assertEqual(item.names[1].end,"9.0")
        self.assertEqual(item.names[1].type,"Attribute")
        self.assertEqual(item.names[2].name,"TestName1")
        self.assertEqual(item.names[2].start,"9.1")
        self.assertEqual(item.names[2].end,"9.1")
        self.assertEqual(item.names[2].type,"Element")
        self.assertEqual(item.names[3].name,"TestName1")
        self.assertEqual(item.names[3].start,"9.3")
        self.assertEqual(item.names[3].end,"9.6")
        self.assertEqual(item.names[3].type,"Element")
        self.assertEqual(item.names[4].name,"TestName2")
        self.assertEqual(item.names[4].start,"9.7")
        self.assertEqual(item.names[4].end,"9.7")
        self.assertEqual(item.names[4].type,"Element")
        self.assertEqual(item.names[5].name,"TestName1")
        self.assertEqual(item.names[5].start,"9.8")
        self.assertEqual(item.names[5].end,"9.8")
        self.assertEqual(item.names[5].type,"Element")

    """
    Tests the addNameForVersion method with duplicates.
    """
    def testAddNameForVersionDuplicates(self):
        # Create a versioned item and add names.
        item = XSDVersionDiffer.VersionedItem("type")
        item.addNameForVersion("TestName1","8.4","Element")
        item.addNameForVersion("TestName1","8.5","Element")
        item.addNameForVersion("TestName1","8.5","Element")

        # Assert duplicate entries aren't created.
        self.assertEqual(len(item.names),2)
        self.assertEqual(item.names[0].name,"TestName1")
        self.assertEqual(item.names[0].start,"8.4")
        self.assertEqual(item.names[0].end,"8.4")
        self.assertEqual(item.names[0].type,"Element")
        self.assertEqual(item.names[1].name,"TestName1")
        self.assertEqual(item.names[1].start,"8.5")
        self.assertEqual(item.names[1].end,"8.5")
        self.assertEqual(item.names[1].type,"Element")



class VersionedCompositeTests(unittest.TestCase):
    """
    Tests the mergeNameVersions method.
    """
    def testMergeNameVersions(self):
        # Create a versioned item and add names.
        item = XSDVersionDiffer.VersionedComposite("type")
        item.addNameForVersion("TestName1","1.0")
        item.addNameForVersion("TestName1","1.1")
        item.addNameForVersion("TestName1","1.2")
        item.addNameForVersion("TestName2","1.3")
        item.addNameForVersion("TestName2","1.4")
        item.addChildNameForVersion("TestElement1","TestElement1","type","1.0")
        item.addChildNameForVersion("TestElement1","TestElement1A","type","1.1")
        item.addChildNameForVersion("TestElement1","TestElement1","type","1.2")
        item.addChildNameForVersion("TestElement1","TestElement1","type","1.3")

        item.addChildNameForVersion("TestElement2","TestElement2","type","1.1")
        item.addChildNameForVersion("TestElement2","TestElement2","type","1.2")
        item.addChildNameForVersion("TestElement2","TestElement2","type","1.3")
        item.addChildNameForVersion("TestElement2","TestElement2","type","1.4")

        item.addChildNameForVersion("TestElement3","TestElement3","type","1.1")
        item.addChildNameForVersion("TestElement3","TestElement3","type","1.2")
        item.addChildNameForVersion("TestElement3","TestElement3","type","1.4")

        # Merge the names and assert the merge was correct.
        item.mergeNameVersions(["1.0","1.1","1.2","1.3","1.4"])
        self.assertEqual(len(item.names),2)
        self.assertEqual(item.names[0].name,"TestName1")
        self.assertEqual(item.names[0].start,"1.0")
        self.assertEqual(item.names[0].end,"1.2")
        self.assertEqual(item.names[0].type,None)
        self.assertEqual(item.names[1].name,"TestName2")
        self.assertEqual(item.names[1].start,"1.3")
        self.assertEqual(item.names[1].end,"1.4")
        self.assertEqual(item.names[1].type,None)
        self.assertEqual(len(item.childItems["TestElement1"].names),3)
        self.assertEqual(item.childItems["TestElement1"].names[0].name,"TestElement1")
        self.assertEqual(item.childItems["TestElement1"].names[0].start,"1.0")
        self.assertEqual(item.childItems["TestElement1"].names[0].end,"1.0")
        self.assertEqual(item.childItems["TestElement1"].names[0].type,None)
        self.assertEqual(item.childItems["TestElement1"].names[1].name,"TestElement1A")
        self.assertEqual(item.childItems["TestElement1"].names[1].start,"1.1")
        self.assertEqual(item.childItems["TestElement1"].names[1].end,"1.1")
        self.assertEqual(item.childItems["TestElement1"].names[1].type,None)
        self.assertEqual(item.childItems["TestElement1"].names[2].name,"TestElement1")
        self.assertEqual(item.childItems["TestElement1"].names[2].start,"1.2")
        self.assertEqual(item.childItems["TestElement1"].names[2].end,"1.3")
        self.assertEqual(item.childItems["TestElement1"].names[2].type,None)
        self.assertEqual(len(item.childItems["TestElement2"].names),1)
        self.assertEqual(item.childItems["TestElement2"].names[0].name,"TestElement2")
        self.assertEqual(item.childItems["TestElement2"].names[0].start,"1.1")
        self.assertEqual(item.childItems["TestElement2"].names[0].end,"1.4")
        self.assertEqual(item.childItems["TestElement2"].names[0].type,None)
        self.assertEqual(len(item.childItems["TestElement3"].names),2)
        self.assertEqual(item.childItems["TestElement3"].names[0].name,"TestElement3")
        self.assertEqual(item.childItems["TestElement3"].names[0].start,"1.1")
        self.assertEqual(item.childItems["TestElement3"].names[0].end,"1.2")
        self.assertEqual(item.childItems["TestElement3"].names[0].type,None)
        self.assertEqual(item.childItems["TestElement3"].names[1].name,"TestElement3")
        self.assertEqual(item.childItems["TestElement3"].names[1].start,"1.4")
        self.assertEqual(item.childItems["TestElement3"].names[1].end,"1.4")
        self.assertEqual(item.childItems["TestElement3"].names[1].type,None)



class VersionedXSDTests(unittest.TestCase):
    """
    Tests the addSimpleType method.
    """
    def testAddSimpleType(self):
        # Create several simple types.
        simpleType1 = XSDData.XSDSimpleType("Test1","string")
        simpleType2A = XSDData.XSDSimpleType("Test2","string")
        simpleType2A.enums = ["Enum1","Enum2","Enum3"]
        simpleType2B = XSDData.XSDSimpleType("Test2","string")
        simpleType2B.enums = ["Enum1","Enum2","Enum3","Enum4"]
        simpleType3 = XSDData.XSDSimpleType("Test3","int")

        # Create the versioned XSD and add the simple types.
        xsd = XSDVersionDiffer.VersionedXSD()
        xsd.addSimpleType(simpleType1,"1.0")
        xsd.addSimpleType(simpleType2A,"1.0")
        xsd.addSimpleType(simpleType1,"1.1")
        xsd.addSimpleType(simpleType2B,"1.1")
        xsd.addSimpleType(simpleType2A,"1.2")
        xsd.addSimpleType(simpleType3,"1.2")

        # Assert the simple types were added correctly.
        self.assertEqual(len(xsd.simpleTypes),2)
        self.assertEqual(xsd.simpleTypes["Test1"].type,"string")
        self.assertEqual(len(xsd.simpleTypes["Test1"].names),2)
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].name,"Test1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].start,"1.0")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].end,"1.0")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].type,None)
        self.assertEqual(xsd.simpleTypes["Test1"].names[1].name,"Test1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[1].start,"1.1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[1].end,"1.1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[1].type,None)
        self.assertEqual(xsd.simpleTypes["Test3"].type,"int")
        self.assertEqual(len(xsd.simpleTypes["Test3"].names),1)
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].name,"Test3")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].start,"1.2")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].end,"1.2")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].type,None)

        # Assert the enums were added correctly.
        self.assertEqual(len(xsd.enums),1)
        self.assertEqual(xsd.enums["Test2"].type,"string")
        self.assertEqual(len(xsd.enums["Test2"].names),3)
        self.assertEqual(xsd.enums["Test2"].names[0].name,"Test2")
        self.assertEqual(xsd.enums["Test2"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].names[0].end,"1.0")
        self.assertEqual(xsd.enums["Test2"].names[0].type,None)
        self.assertEqual(xsd.enums["Test2"].names[1].name,"Test2")
        self.assertEqual(xsd.enums["Test2"].names[1].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].names[1].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].names[1].type,None)
        self.assertEqual(xsd.enums["Test2"].names[2].name,"Test2")
        self.assertEqual(xsd.enums["Test2"].names[2].start,"1.2")
        self.assertEqual(xsd.enums["Test2"].names[2].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].names[2].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems),4)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum1"].names),3)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].name,"Enum1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].end,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[1].name,"Enum1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[1].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[1].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[1].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[2].name,"Enum1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[2].start,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[2].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[2].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum2"].names),3)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].name,"Enum2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].end,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[1].name,"Enum2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[1].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[1].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[1].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[2].name,"Enum2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[2].start,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[2].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[2].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum3"].names),3)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].name,"Enum3")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].end,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[1].name,"Enum3")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[1].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[1].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[1].type,None)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[2].name,"Enum3")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[2].start,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[2].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[2].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum4"].names),1)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].name,"Enum4")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].type,None)

        # Merge the XSDs together.
        xsd.mergeNameVersions(["1.0","1.1","1.2"])

        # Assert the merged simple types are correct.
        self.assertEqual(len(xsd.simpleTypes),2)
        self.assertEqual(xsd.simpleTypes["Test1"].type,"string")
        self.assertEqual(len(xsd.simpleTypes["Test1"].names),1)
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].name,"Test1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].start,"1.0")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].end,"1.1")
        self.assertEqual(xsd.simpleTypes["Test1"].names[0].type,None)
        self.assertEqual(xsd.simpleTypes["Test3"].type,"int")
        self.assertEqual(len(xsd.simpleTypes["Test3"].names),1)
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].name,"Test3")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].start,"1.2")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].end,"1.2")
        self.assertEqual(xsd.simpleTypes["Test3"].names[0].type,None)

        # Assert the merged enums are correct.
        self.assertEqual(len(xsd.enums),1)
        self.assertEqual(xsd.enums["Test2"].type,"string")
        self.assertEqual(len(xsd.enums["Test2"].names),1)
        self.assertEqual(xsd.enums["Test2"].names[0].name,"Test2")
        self.assertEqual(xsd.enums["Test2"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].names[0].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].names[0].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems),4)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum1"].names),1)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].name,"Enum1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum1"].names[0].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum2"].names),1)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].name,"Enum2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum2"].names[0].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum3"].names),1)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].name,"Enum3")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].start,"1.0")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].end,"1.2")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum3"].names[0].type,None)
        self.assertEqual(len(xsd.enums["Test2"].childItems["Enum4"].names),1)
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].name,"Enum4")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].start,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].end,"1.1")
        self.assertEqual(xsd.enums["Test2"].childItems["Enum4"].names[0].type,None)

    """
    Tests the addComplexType method.
    """
    def testAddComplexType(self):
        # Create several complex types.
        testChildElement = XSDData.XSDChildElement("Test","string")
        testAttribute = XSDData.XSDAttribute("Test","string")
        testElement1 = XSDData.XSDComplexType("litleRequest",None)
        testElement2 = XSDData.XSDComplexType("litleRequest",None)
        testElement2.childItems = [testChildElement]
        testElement3 = XSDData.XSDComplexType("cnpRequest",None)
        testElement3.childItems = [testAttribute]

        # Create the versioned XSD and add the complex types.
        xsd = XSDVersionDiffer.VersionedXSD()
        xsd.addComplexType(testElement1,"1.0")
        xsd.addComplexType(testElement2,"1.1")
        xsd.addComplexType(testElement3,"1.2")
        xsd.addComplexType(testElement3,"1.3")

        # Assert the complex type was added correctly.
        self.assertEqual(len(xsd.complexTypes),1)
        self.assertEqual(xsd.complexTypes["cnpRequest"].type,None)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].names),4)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].start,"1.0")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].end,"1.0")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].name,"litleRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].type,None)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].start,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].end,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].name,"litleRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].type,None)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[2].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[2].end,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[2].name,"cnpRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[2].type,None)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[3].start,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[3].end,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[3].name,"cnpRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[3].type,None)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].childItems.keys()),1)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].childItems["Test"].names),3)
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].start,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].end,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].type,"Element")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].end,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].type,"Attribute")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[2].start,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[2].end,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[2].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[2].type,"Attribute")

        # Merge the XSDs together.
        xsd.mergeNameVersions(["1.0","1.1","1.2","1.3"])

        # Assert the merged complex type is correct.
        self.assertEqual(len(xsd.complexTypes.keys()),1)
        self.assertEqual(xsd.complexTypes["cnpRequest"].type,None)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].names),2)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].start,"1.0")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].end,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].name,"litleRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[0].type,None)
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].end,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].name,"cnpRequest")
        self.assertEqual(xsd.complexTypes["cnpRequest"].names[1].type,None)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].childItems.keys()),1)
        self.assertEqual(len(xsd.complexTypes["cnpRequest"].childItems["Test"].names),2)
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].start,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].end,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[0].type,"Element")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].end,"1.3")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest"].childItems["Test"].names[1].type,"Attribute")

    """
    Tests merging superclass items in complex types.
    """
    def testMergingSuperclasses(self):
        # Create several complex types.
        testChildElement = XSDData.XSDChildElement("Test","string")
        testAttribute = XSDData.XSDAttribute("Test","string")
        testElement1 = XSDData.XSDComplexType("cnpRequest1",None)
        testElement1.childItems = [testChildElement,XSDData.XSDChildElement("Test3","string")]
        testElement2 = XSDData.XSDComplexType("cnpRequest2","cnpRequest1")
        testElement2.childItems = [testChildElement]
        testElement3 = XSDData.XSDComplexType("cnpRequest3","cnpRequest2")
        testElement3.childItems = [testAttribute,XSDData.XSDChildElement("Test2","string")]

        # Create the versioned XSD and add the complex types.
        xsd = XSDVersionDiffer.VersionedXSD()
        xsd.addComplexType(testElement1,"1.0")
        xsd.addComplexType(testElement2,"1.1")
        xsd.addComplexType(testElement3,"1.2")

        # Assert the findings of implementation are correct.
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest3","Test"),"cnpRequest3")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest3","Test2"),"cnpRequest3")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest3","Test3"),"cnpRequest1")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest2","Test"),"cnpRequest2")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest2","Test2"),None)
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest2","Test3"),"cnpRequest1")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest1","Test"),"cnpRequest1")
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest1","Test2"),None)
        self.assertEqual(xsd.getComplexTypeWithChild("cnpRequest1","Test3"),"cnpRequest1")

        # Merge the XSDs together.
        xsd.mergeNameVersions(["1.0","1.1","1.2"])

        # Assert the merged complex type is correct.
        self.assertEqual(len(xsd.complexTypes.keys()),3)
        self.assertEqual(xsd.complexTypes["cnpRequest1"].type,None)
        self.assertEqual(xsd.complexTypes["cnpRequest2"].type,"cnpRequest1")
        self.assertEqual(xsd.complexTypes["cnpRequest3"].type,"cnpRequest2")
        self.assertEqual(len(xsd.complexTypes["cnpRequest1"].childItems.keys()),2)
        self.assertEqual(len(xsd.complexTypes["cnpRequest1"].childItems["Test"].names),2)
        self.assertEqual(len(xsd.complexTypes["cnpRequest1"].childItems["Test3"].names),1)
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[0].start,"1.0")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[0].end,"1.1")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[0].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[0].type,"Element")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[1].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[1].end,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[1].name,"Test")
        self.assertEqual(xsd.complexTypes["cnpRequest1"].childItems["Test"].names[1].type,"Attribute")
        self.assertEqual(len(xsd.complexTypes["cnpRequest2"].childItems.keys()),0)
        self.assertEqual(len(xsd.complexTypes["cnpRequest3"].childItems.keys()),1)
        self.assertEqual(xsd.complexTypes["cnpRequest3"].childItems["Test2"].names[0].start,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest3"].childItems["Test2"].names[0].end,"1.2")
        self.assertEqual(xsd.complexTypes["cnpRequest3"].childItems["Test2"].names[0].name,"Test2")
        self.assertEqual(xsd.complexTypes["cnpRequest3"].childItems["Test2"].names[0].type,"Element")