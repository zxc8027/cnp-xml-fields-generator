"""
Zachary Cook

Tests the XSD parser.
"""

import unittest
from Parser.XSDParser import XSDParser, XSDData



class XSDParserTests(unittest.TestCase):
    """
    Tests checking if types are valid for error checking.
    """
    def testIsTypeValid(self):
        # Create an XSD.
        xsd = XSDParser.XSD()
        xsd.addType(XSDData.XSDSimpleType("test1","string"))
        xsd.addType(XSDData.XSDSimpleType("test2","boolean"))
        xsd.addType(XSDData.XSDSimpleType("test3","int"))
        xsd.addType(XSDData.XSDComplexType("test4","string"))
        xsd.addType(XSDData.XSDComplexType("test5","test2"))
        xsd.addType(XSDData.XSDComplexType("test6","test4"))
        xsd.addType(XSDData.XSDComplexType("test7","test8"))

        # Assert the types are valid.
        self.assertTrue(xsd.isTypeValid("test1"))
        self.assertTrue(xsd.isTypeValid("test2"))
        self.assertTrue(xsd.isTypeValid("test3"))
        self.assertTrue(xsd.isTypeValid("test4"))
        self.assertTrue(xsd.isTypeValid("test5"))
        self.assertTrue(xsd.isTypeValid("test6"))
        self.assertFalse(xsd.isTypeValid("test7"))
        self.assertFalse(xsd.isTypeValid("test8"))

    """
    Tests parsing a simpleType without enumeration.
    """
    def testSimpleTypeWithoutEnumeration(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
              "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
              "    <xs:simpleType name=\"stringMin1Max36CollapseWhiteSpaceType\">" \
              "        <xs:restriction base=\"xs:string\">" \
              "            <xs:minLength value=\"1\" />" \
              "            <xs:maxLength value=\"36\" />" \
              "            <xs:whiteSpace value=\"collapse\"/>" \
              "        </xs:restriction>" \
              "    </xs:simpleType>" \
              "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("stringMin1Max36CollapseWhiteSpaceType")
        self.assertEqual(simpleType.name,"stringMin1Max36CollapseWhiteSpaceType")
        self.assertEqual(simpleType.base,"string")
        self.assertEqual(simpleType.isEnum(),False)
        self.assertEqual(simpleType.restrictions,{"minLength":"1","maxLength":"36","whiteSpace":"collapse"})
        self.assertEqual(simpleType.enums,[])

    """
    Tests parsing a simpleType with enumeration.
    """
    def testSimpleTypeWithEnumeration(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
              "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
              "    <xs:simpleType name=\"currencyCodeEnum\">" \
              "        <xs:restriction base=\"xs:string\">" \
              "            <xs:enumeration value=\"AUD\" />" \
              "            <xs:enumeration value=\"CAD\" />" \
              "            <xs:enumeration value=\"CHF\" />" \
              "            <xs:enumeration value=\"DKK\" />" \
              "            <xs:enumeration value=\"EUR\" />" \
              "            <xs:enumeration value=\"GBP\" />" \
              "            <xs:enumeration value=\"HKD\" />" \
              "            <xs:enumeration value=\"JPY\" />" \
              "            <xs:enumeration value=\"NOK\" />" \
              "            <xs:enumeration value=\"NZD\" />" \
              "            <xs:enumeration value=\"SEK\" />" \
              "            <xs:enumeration value=\"SGD\" />" \
              "            <xs:enumeration value=\"USD\" />" \
              "        </xs:restriction>" \
              "    </xs:simpleType>" \
              "</xs:schema>"


        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("currencyCodeEnum")
        self.assertEqual(simpleType.name,"currencyCodeEnum")
        self.assertEqual(simpleType.base,"string")
        self.assertEqual(simpleType.isEnum(),True)
        self.assertEqual(simpleType.restrictions,{})
        self.assertEqual(simpleType.enums,["AUD","CAD","CHF","DKK","EUR","GBP","HKD","JPY","NOK","NZD","SEK","SGD","USD"])

    """
    Tests parsing an element with no complex type.
    """
    def testElementNoComplexType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"card\" substitutionGroup=\"xp:cardOrToken\" type=\"xp:cardType\"/>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getElement("card")
        self.assertEqual(element.name,"card")
        self.assertEqual(element.base,"cardType")

    """
    Tests parsing a complex type element with no base and no restriction.
    """
    def testComplexTypeElementBasic(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"authentication\">" \
                  "        <xs:complexType>" \
                  "            <xs:sequence>" \
                  "                <xs:element name=\"user\" type=\"xp:string20Type\" />" \
                  "                <xs:element name=\"password\" type=\"xp:string20Type\" />" \
                  "            </xs:sequence>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("authentication")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0],XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"sequence")
        self.assertEqual(len(element.childItems[0].childItems),2)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[0].name,"user")
        self.assertEqual(element.childItems[0].childItems[0].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[0].default,None)
        self.assertEqual(element.childItems[0].childItems[0].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[0].maxOccurrences,1)
        self.assertIsInstance(element.childItems[0].childItems[1],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[1].name,"password")
        self.assertEqual(element.childItems[0].childItems[1].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[1].default,None)
        self.assertEqual(element.childItems[0].childItems[1].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[1].maxOccurrences,1)

    """
    Tests a complex type being separate from the element.
    """
    def testTypeAndElementNameCollision(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"updateCardValidationNumOnToken\" substitutionGroup=\"xp:transaction\" type=\"xp:updateCardValidationNumOnToken\"/>" \
                  "     " \
                  "     <xs:complexType name=\"updateCardValidationNumOnToken\">" \
                  "        <xs:complexContent>" \
                  "            <xs:extension base=\"xp:transactionTypeWithReportGroup\">" \
                  "                <xs:sequence>" \
                  "                    <xs:element name=\"orderId\" type=\"xp:string25Type\" minOccurs=\"0\" />" \
                  "                    <xs:element name=\"cnpToken\" type=\"xp:ccAccountNumberType\" />" \
                  "                    <xs:element name=\"cardValidationNum\" type=\"xp:cvNumType\"/>" \
                  "                </xs:sequence>" \
                  "            </xs:extension>" \
                  "        </xs:complexContent>" \
                  "    </xs:complexType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getElement("updateCardValidationNumOnToken")
        complexType = xsd.getType("updateCardValidationNumOnToken")
        self.assertEqual(element.name,"updateCardValidationNumOnToken")
        self.assertEqual(element.base,"updateCardValidationNumOnToken")
        self.assertEqual(complexType.name,"updateCardValidationNumOnToken")
        self.assertEqual(complexType.base,"transactionTypeWithReportGroup")

    """
    Tests merging 2 simple types.
    """
    def testMergeSimpleType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "     <xs:simpleType name=\"customType\">" \
                  "         <xs:restriction base=\"xs:string\">" \
                  "             <xs:enumeration value=\"OneTime\" />" \
                  "             <xs:enumeration value=\"FirstRecurring\" />" \
                  "             <xs:enumeration value=\"SubsequentRecurring\" />" \
                  "             <xs:enumeration value=\"FinalRecurring\" />" \
                  "         </xs:restriction>" \
                  "     </xs:simpleType>" \
                  "     " \
                  "     <xs:simpleType name=\"customType\">" \
                  "         <xs:restriction base=\"xs:string\">" \
                  "             <xs:pattern value=\"[0-9]{6}|0\"/>" \
                  "         </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("customType")
        self.assertEqual(simpleType.name,"customType")
        self.assertEqual(simpleType.base,"string")
        self.assertEqual(simpleType.isEnum(),True)
        self.assertEqual(simpleType.restrictions,{"pattern": "[0-9]{6}|0"})
        self.assertEqual(simpleType.enums,["OneTime","FirstRecurring","SubsequentRecurring","FinalRecurring"])

    """
    Tests merging 2 complex types.
    """
    def testMergeComplexType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:complexType name=\"authentication\">" \
                  "        <xs:sequence>" \
                  "            <xs:element name=\"user\" type=\"xp:string20Type\" />" \
                  "        </xs:sequence>" \
                  "    </xs:complexType>" \
                  "    <xs:complexType name=\"authentication\">" \
                  "        <xs:sequence>" \
                  "            <xs:element name=\"password\" type=\"xp:string20Type\" />" \
                  "        </xs:sequence>" \
                  "    </xs:complexType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        complexType = xsd.getType("authentication")
        self.assertEqual(complexType.name,"authentication")
        self.assertEqual(complexType.base,None)
        self.assertEqual(len(complexType.childItems),2)

    """
    Tests attributes being required and optional.
    """
    def testUseInAttributes(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:attribute name=\"attribute1\" type=\"xp:string20Type\" use=\"required\"/>" \
                  "                <xs:attribute name=\"attribute2\" type=\"xp:string20Type\" use=\"optional\"/>" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("customElement")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0], XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"all")
        self.assertEqual(len(element.childItems[0].childItems),2)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDAttribute)
        self.assertEqual(element.childItems[0].childItems[0].name,"attribute1")
        self.assertEqual(element.childItems[0].childItems[0].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[0].required,True)
        self.assertEqual(element.childItems[0].childItems[0].default,None)
        self.assertIsInstance(element.childItems[0].childItems[1],XSDData.XSDAttribute)
        self.assertEqual(element.childItems[0].childItems[1].name,"attribute2")
        self.assertEqual(element.childItems[0].childItems[1].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[1].required,False)
        self.assertEqual(element.childItems[0].childItems[1].default,None)

    """
    Tests elements having custom occurrences.
    """
    def testElementOccurrences(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"authentication\">" \
                  "        <xs:complexType>" \
                  "            <xs:sequence>" \
                  "                <xs:element name=\"user\" type=\"xp:string20Type\" minOccurs=\"2\" maxOccurs=\"6\"/>" \
                  "                <xs:element name=\"password\" type=\"xp:string20Type\" maxOccurs=\"unbounded\" />" \
                  "            </xs:sequence>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("authentication")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0],XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"sequence")
        self.assertEqual(len(element.childItems[0].childItems),2)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[0].name,"user")
        self.assertEqual(element.childItems[0].childItems[0].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[0].default,None)
        self.assertEqual(element.childItems[0].childItems[0].minOccurrences,2)
        self.assertEqual(element.childItems[0].childItems[0].maxOccurrences,6)
        self.assertIsInstance(element.childItems[0].childItems[1],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[1].name,"password")
        self.assertEqual(element.childItems[0].childItems[1].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[1].default,None)
        self.assertEqual(element.childItems[0].childItems[1].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[1].maxOccurrences,(2 ** 31) - 1)

    """
    Tests attributes and elements having defaults.
    """
    def testDefaults(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:attribute name=\"attribute1\" type=\"xp:string20Type\" default=\"value1\"/>" \
                  "                <xs:element name=\"attribute2\" type=\"xp:string20Type\" default=\"value2\"/>" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("customElement")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0], XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"all")
        self.assertEqual(len(element.childItems[0].childItems),2)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDAttribute)
        self.assertEqual(element.childItems[0].childItems[0].name,"attribute1")
        self.assertEqual(element.childItems[0].childItems[0].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[0].required,False)
        self.assertEqual(element.childItems[0].childItems[0].default,"value1")
        self.assertIsInstance(element.childItems[0].childItems[1],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[1].name,"attribute2")
        self.assertEqual(element.childItems[0].childItems[1].type,"string20Type")
        self.assertEqual(element.childItems[0].childItems[1].default,"value2")
        self.assertEqual(element.childItems[0].childItems[1].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[1].maxOccurrences,1)

    """
    Tests an element having an embedded simple type.
    """
    def testEmbeddedSimpleType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:simpleType>" \
                  "            <xs:restriction base=\"xs:string\">" \
                  "                <xs:minLength value=\"1\" />" \
                  "            </xs:restriction>" \
                  "        </xs:simpleType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(len(xsd.types),1)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("customElement")
        self.assertEqual(element.name,"customElement")
        self.assertEqual(element.base,"string")
        self.assertEqual(element.isEnum(),False)
        self.assertEqual(element.restrictions,{"minLength": "1"})
        self.assertEqual(element.enums,[])

    """
    Tests an element having an embedded complex type.
    """
    def testEmbeddedComplexType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:element name=\"customType\">" \
                  "                    <xs:complexType>" \
                  "                        <xs:choice>" \
                  "                            <xs:element name=\"customElement\" type=\"xs:string\"/>" \
                  "                        </xs:choice>" \
                  "                    </xs:complexType>" \
                  "                </xs:element>" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(len(xsd.types),2)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("customElement")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0], XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"all")
        self.assertEqual(len(element.childItems[0].childItems),1)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[0].name,"customType")
        self.assertEqual(element.childItems[0].childItems[0].type,"customType")
        self.assertEqual(element.childItems[0].childItems[0].default,None)
        self.assertEqual(element.childItems[0].childItems[0].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[0].maxOccurrences,1)

    """
    Tests an element being only a reference to a type.
    """
    def testReference(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:element ref=\"customSubElement\" />" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        element = xsd.getType("customElement")
        self.assertEqual(len(element.childItems),1)
        self.assertIsInstance(element.childItems[0],XSDData.XSDGroup)
        self.assertEqual(element.childItems[0].type,"all")
        self.assertEqual(len(element.childItems[0].childItems),1)
        self.assertIsInstance(element.childItems[0].childItems[0],XSDData.XSDChildElement)
        self.assertEqual(element.childItems[0].childItems[0].name,"customSubElement")
        self.assertEqual(element.childItems[0].childItems[0].type,"customSubElement")
        self.assertEqual(element.childItems[0].childItems[0].default,None)
        self.assertEqual(element.childItems[0].childItems[0].minOccurrences,0)
        self.assertEqual(element.childItems[0].childItems[0].maxOccurrences,1)

    """
    Tests the flattenXSD method.
    """
    def testFlattenXSD(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:simpleType name=\"stringMin1Max36CollapseWhiteSpaceType\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "            <xs:maxLength value=\"36\" />" \
                  "            <xs:whiteSpace value=\"collapse\"/>" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:element name=\"createPlan\" substitutionGroup=\"xp:recurringTransaction\" >" \
                  "        <xs:complexType>" \
                  "            <xs:complexContent>" \
                  "                <xs:extension base=\"xp:recurringTransactionType\">" \
                  "                    <xs:sequence>" \
                  "                        <xs:attribute name=\"attribute\" type=\"string\"/>" \
                  "                        <xs:element name=\"element1\" type=\"string\"/>" \
                  "                        <xs:all>" \
                  "                            <xs:element name=\"element2\" type=\"string\"/>" \
                  "                            <xs:sequence>" \
                  "                                <xs:element name=\"element3\" type=\"string\"/>" \
                  "                            </xs:sequence>" \
                  "                        </xs:all>" \
                  "                    </xs:sequence>" \
                  "                </xs:extension>" \
                  "            </xs:complexContent>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"


        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        xsd = XSDParser.flattenXSD(xsd)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("stringMin1Max36CollapseWhiteSpaceType")
        self.assertEqual(simpleType.name,"stringMin1Max36CollapseWhiteSpaceType")
        self.assertEqual(simpleType.base,"string")
        self.assertEqual(simpleType.isEnum(),False)
        self.assertEqual(simpleType.restrictions,{"minLength": "1", "maxLength": "36", "whiteSpace": "collapse"})
        self.assertEqual(simpleType.enums,[])
        element = xsd.getElement("createPlan")
        self.assertEqual(element.name,"createPlan")
        self.assertEqual(element.base,"recurringTransaction")
        complexType = xsd.getType("createPlan")
        self.assertEqual(complexType.name,"createPlan")
        self.assertEqual(complexType.base,"recurringTransactionType")
        self.assertEqual(len(complexType.childItems),4)
        self.assertEqual(complexType.childItems[0].name,"attribute")
        self.assertEqual(complexType.childItems[0].type,"string")
        self.assertEqual(complexType.childItems[1].name,"element1")
        self.assertEqual(complexType.childItems[1].type,"string")
        self.assertEqual(complexType.childItems[2].name,"element2")
        self.assertEqual(complexType.childItems[2].type,"string")
        self.assertEqual(complexType.childItems[3].name,"element3")
        self.assertEqual(complexType.childItems[3].type,"string")

    """
    Tests the getRootBaseType method.
    """
    def testGetRootBaseType(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:simpleType name=\"testSimpleType1\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType2\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType3\">" \
                  "        <xs:restriction base=\"xs:integer\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace, "http://www.vantivcnp.com/schema")
        self.assertEqual(xsd.getRootBaseType("testSimpleType1"),"string")
        self.assertEqual(xsd.getRootBaseType("testSimpleType2"),"string")
        self.assertEqual(xsd.getRootBaseType("testSimpleType3"),"integer")

    """
    Tests the compressXSD method.
    """
    def testCompressXSD(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:simpleType name=\"testSimpleType1\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType2\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType3\">" \
                  "        <xs:restriction base=\"xs:integer\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType4\">" \
                  "        <xs:restriction base=\"xs:unknown\">" \
                  "            <xs:minLength value=\"1\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:simpleType name=\"testSimpleType5\">" \
                  "        <xs:restriction base=\"xs:string\">" \
                  "            <xs:enumeration value=\"value1\" />" \
                  "            <xs:enumeration value=\"value2\" />" \
                  "            <xs:enumeration value=\"value3\" />" \
                  "        </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "    " \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:element name=\"element1\" type=\"testSimpleType1\" />" \
                  "                <xs:element name=\"element2\" type=\"testSimpleType2\" />" \
                  "                <xs:element name=\"element3\" type=\"testSimpleType3\" />" \
                  "                <xs:element name=\"element4\" type=\"testSimpleType4\" />" \
                  "                <xs:element name=\"element5\" type=\"testSimpleType5\" />" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        xsd = XSDParser.flattenXSD(xsd)
        xsd = XSDParser.compressXSD(xsd)
        self.assertEqual(xsd.namespace, "http://www.vantivcnp.com/schema")
        self.assertIsNone(xsd.getType("testSimpleType1"))
        self.assertIsNone(xsd.getType("testSimpleType2"))
        self.assertIsNone(xsd.getType("testSimpleType3"))
        simpleType = xsd.getType("testSimpleType4")
        self.assertEqual(simpleType.name,"testSimpleType4")
        self.assertEqual(simpleType.base,"unknown")
        simpleEnum = xsd.getType("testSimpleType5")
        self.assertEqual(simpleEnum.name,"testSimpleType5")
        self.assertEqual(simpleEnum.base,"string")
        self.assertEqual(simpleEnum.enums,["value1","value2","value3"])
        simpleEnum = xsd.getType("customElement")
        self.assertEqual(simpleEnum.name,"customElement")
        self.assertEqual(simpleEnum.childItems[0].type,"string")
        self.assertEqual(simpleEnum.childItems[1].type,"string")
        self.assertEqual(simpleEnum.childItems[2].type,"integer")
        self.assertEqual(simpleEnum.childItems[3].type,"testSimpleType4")
        self.assertEqual(simpleEnum.childItems[4].type,"testSimpleType5")

    """
    Tests the compressXSD method with element references.
    """
    def testCompressXSDElementReferences(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:complexType name=\"type1\">" \
                  "        <xs:all>" \
                  "            <xs:element name=\"element\" type=\"string\" />" \
                  "        </xs:all>" \
                  "    </xs:complexType>" \
                  "    " \
                  "    <xs:complexType name=\"type2\">" \
                  "        <xs:all>" \
                  "            <xs:element name=\"element\" type=\"string\" />" \
                  "        </xs:all>" \
                  "    </xs:complexType>" \
                  "    " \
                  "    <xs:element name=\"type3\" type=\"type1\" />" \
                  "    " \
                  "    <xs:element name=\"type2\" type=\"type2\" />" \
                  "    " \
                  "    <xs:element name=\"type4\" type=\"type3\" />" \
                  "    " \
                  "    <xs:element name=\"customElement\">" \
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:element name=\"element1\" type=\"type1\" />" \
                  "                <xs:element name=\"element2\" type=\"type2\" />" \
                  "                <xs:element name=\"element3\" type=\"type3\" />" \
                  "                <xs:element name=\"element4\" type=\"type4\" />" \
                  "            </xs:all>" \
                  "        </xs:complexType>" \
                  "    </xs:element>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        xsd = XSDParser.flattenXSD(xsd)
        xsd = XSDParser.compressXSD(xsd)
        self.assertEqual(xsd.namespace, "http://www.vantivcnp.com/schema")
        simpleEnum = xsd.getType("customElement")
        self.assertEqual(simpleEnum.name,"customElement")
        self.assertEqual(simpleEnum.childItems[0].type,"type1")
        self.assertEqual(simpleEnum.childItems[1].type,"type2")
        self.assertEqual(simpleEnum.childItems[2].type,"type1")
        self.assertEqual(simpleEnum.childItems[3].type,"type1")