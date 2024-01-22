import unittest

from src.main.python.nwselect import main as nwselect


class TestIPV4Match(unittest.TestCase):
    def test_positive(self):
        self.assertTrue(nwselect.is_valid_ipv4("1.2.3.4"))
        self.assertTrue(nwselect.is_valid_ipv4("255.255.255.255"))
        self.assertTrue(nwselect.is_valid_ipv4("25.25.25.25"))
        self.assertTrue(nwselect.is_valid_ipv4("0.0.0.0"))

    def test_negative(self):
        self.assertFalse(nwselect.is_valid_ipv4("I'm a little teapot"))
        self.assertFalse(nwselect.is_valid_ipv4("256.255.255.255"))
        self.assertFalse(nwselect.is_valid_ipv4("261.255.255.255"))
        self.assertFalse(nwselect.is_valid_ipv4("-25.25.25.25"))
        self.assertFalse(nwselect.is_valid_ipv4("1000.1000.1000.1000"))
        self.assertFalse(nwselect.is_valid_ipv4("fd01:c450:37a5:10:6c:e355:4550:5a7c"))


