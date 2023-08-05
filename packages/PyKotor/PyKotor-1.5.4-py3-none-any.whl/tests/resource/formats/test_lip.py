import platform
from unittest import TestCase

from pykotor.resource.formats.lip import LIP, LIPShape, LIPBinaryReader, detect_lip, write_lip, LIPXMLReader, read_lip
from pykotor.resource.type import ResourceType

BINARY_TEST_FILE = "../../files/test.lip"
XML_TEST_FILE = "../../files/test.lip.xml"
DOES_NOT_EXIST_FILE = "./thisfiledoesnotexist"
CORRUPT_BINARY_TEST_FILE = "../../files/test_corrupted.lip"
CORRUPT_XML_TEST_FILE = "../../files/test_corrupted.lip.xml"


class TestLIP(TestCase):
    def test_binary_io(self):
        self.assertEqual(detect_lip(BINARY_TEST_FILE), ResourceType.LIP)

        lip = LIPBinaryReader(BINARY_TEST_FILE).load()
        self.validate_io(lip)

        data = bytearray()
        write_lip(lip, data, ResourceType.LIP)
        lip = LIPBinaryReader(data).load()
        self.validate_io(lip)

    def test_xml_io(self):
        self.assertEqual(detect_lip(XML_TEST_FILE), ResourceType.LIP_XML)

        lip = LIPXMLReader(XML_TEST_FILE).load()
        self.validate_io(lip)

        data = bytearray()
        write_lip(lip, data, ResourceType.LIP_XML)
        lip = LIPXMLReader(data).load()
        self.validate_io(lip)

    def validate_io(self, lip: LIP):
        self.assertAlmostEqual(lip.length, 1.50, 3)
        self.assertEqual(LIPShape.EE, lip.get(0).shape)
        self.assertEqual(LIPShape.OOH, lip.get(1).shape)
        self.assertEqual(LIPShape.TH, lip.get(2).shape)
        self.assertAlmostEqual(0.0, lip.get(0).time, 4)
        self.assertAlmostEqual(0.7777, lip.get(1).time, 4)
        self.assertAlmostEqual(1.25, lip.get(2).time, 4)

    def test_read_raises(self):
        if platform.system() == "Windows":
            self.assertRaises(PermissionError, read_lip, ".")
        else:
            self.assertRaises(IsADirectoryError, read_lip, ".")
        self.assertRaises(FileNotFoundError, read_lip, DOES_NOT_EXIST_FILE)
        self.assertRaises(ValueError, read_lip, CORRUPT_BINARY_TEST_FILE)
        self.assertRaises(ValueError, read_lip, CORRUPT_XML_TEST_FILE)

    def test_write_raises(self):
        if platform.system() == "Windows":
            self.assertRaises(PermissionError, write_lip, LIP(), ".", ResourceType.LIP)
        else:
            self.assertRaises(IsADirectoryError, write_lip, LIP(), ".", ResourceType.LIP)
        self.assertRaises(ValueError, write_lip, LIP(), ".", ResourceType.INVALID)
