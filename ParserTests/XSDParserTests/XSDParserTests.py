"""
Zachary Cook

Tests the XSD parser.
"""

import unittest

from Parser.XSDParser import XSDParser


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
    Tests parsing a complex type element with no base and no restriction.
    """
    def testComplexTypeElementBasic(self):
        xsdText = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
                  "<xs:schema targetNamespace=\"http://www.vantivcnp.com/schema\" xmlns:xp=\"http://www.vantivcnp.com/schema\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">" \
                  "    <xs:element name=\"authentication\">" \
                  "        <xs:complexType>" \
                  "            <xs:sequence>" \
                  "                <xs: element name=\"user\" type=\"xp:string20Type\" />" \
                  "                <xs:element name=\"password\" type=\"xp:string20Type\" / >" \
                  "            </xs:sequence>" \
                  "        </xs:complexType>" \
                  "    </xs:simpleType>" \
                  "</xs:schema>"

        # Parse the XSD text and assert it was parsed correctly.
        xsd = XSDParser.processXSD(xsdText)
        self.assertEqual(xsd.namespace, "http://www.vantivcnp.com/schema")
        simpleType = xsd.getType("currencyCodeEnum")
        self.assertEqual(simpleType.name, "currencyCodeEnum")
        self.assertEqual(simpleType.base, "string")
        self.assertEqual(simpleType.isEnum(), True)
        self.assertEqual(simpleType.restrictions, {})
