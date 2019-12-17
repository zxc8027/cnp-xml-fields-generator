"""
Zachary Cook

Tests the XSD parser.
"""

import unittest
from Parser.XSDParser import XSDParser, XSDData



class XSDParserTests(unittest.TestCase):
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
                  "     <xs:simpleType name=\"sequenceType\">" \
                  "         <xs:restriction base=\"xs:string\">" \
                  "             <xs:enumeration value=\"OneTime\"/>" \
                  "             <xs:enumeration value=\"FirstRecurring\"/>" \
                  "             <xs:enumeration value=\"SubsequentRecurring\"/>" \
                  "             <xs:enumeration value=\"FinalRecurring\"/>" \
                  "         </xs:restriction>" \
                  "     </xs:simpleType>" \
                  "     " \
                  "     <xs:simpleType name=\"sequenceType\">" \
                  "         <xs:restriction base=\"xs:string\">" \
                  "             <xs:pattern value=\"[0-9]{6}|0\"/>" \
                  "         </xs:restriction>" \
                  "    </xs:simpleType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace,"http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("sequenceType")
        self.assertEqual(simpleType.name,"sequenceType")
        self.assertEqual(simpleType.base,"string")
        self.assertEqual(simpleType.isEnum(),True)
        self.assertEqual(simpleType.restrictions,{"pattern": "[0-9]{6}|0"})
        self.assertEqual(simpleType.enums,["OneTime","FirstRecurring","SubsequentRecurring","FinalRecurring"])

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
                  "        <xs:complexType>" \
                  "            <xs:all>" \
                  "                <xs:element name=\"customType\">" \
                  "                    <xs:simpleType>" \
                  "                        <xs:restriction base=\"xs:int\">" \
                  "                            <xs:totalDigits value=\"4\"/>" \
                  "                        </xs:restriction>" \
                  "                    </xs:simpleType>" \
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
                  "                            <xs:totalDigits value=\"4\"/>" \
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