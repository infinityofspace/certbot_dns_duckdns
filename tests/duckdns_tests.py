import unittest

from certbot_dns_duckdns.duckdns.client import (
    DuckDNSClient,
    is_valid_duckdns_domain,
    is_valid_full_duckdns_domain,
)

TEST_DOMAIN = "example.duckdns.org"
TEST_DUCKDNS_TOKEN = "1234567890abcdef"


class DuckDNSTests(unittest.TestCase):
    def test_get_validated_root_domain_hyphen_domain(self):
        domain = "test-example.duckdns.org"
        root_domain = DuckDNSClient.__get_validated_root_domain__(domain)
        self.assertEqual(root_domain, domain)

    def test_get_validated_root_domain_multiple_subdomains(self):
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "test1.test2." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "test1.test2.test3." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)

    def test_get_validated_root_domain_special_subdomains(self):
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "test-." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "test--." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "-test." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "--test." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "-." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "--." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "-test-." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "test--test." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "12345." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "12345-." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "12345--." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "-12345." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "--12345." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__(
                "-123ad-sdas--45-as-." + TEST_DOMAIN
            )
            self.assertEqual(root_domain, TEST_DOMAIN)

    def test_is_valid_duckdns_domain(self):
        with self.subTest():
            self.assertTrue(is_valid_duckdns_domain(TEST_DOMAIN))
            self.assertTrue(is_valid_duckdns_domain("test." + TEST_DOMAIN))
            self.assertTrue(is_valid_duckdns_domain("test.abc." + TEST_DOMAIN))
            self.assertTrue(is_valid_duckdns_domain("test.abc.efg." + TEST_DOMAIN))
            self.assertTrue(is_valid_duckdns_domain("test-abc." + TEST_DOMAIN))
            self.assertTrue(is_valid_duckdns_domain("abc.def.ghi"))
            self.assertTrue(is_valid_duckdns_domain("example.com"))
            self.assertTrue(is_valid_duckdns_domain("test.duckduckduck.ababaa"))
            self.assertTrue(is_valid_duckdns_domain("123456"))

        with self.subTest():
            self.assertFalse(is_valid_duckdns_domain("example.com."))
            self.assertFalse(is_valid_duckdns_domain("example.%."))
            self.assertFalse(is_valid_duckdns_domain("$.%."))
            self.assertFalse(is_valid_duckdns_domain("$"))
            self.assertFalse(is_valid_duckdns_domain("1234*"))

    def test_is_valid_full_duckdns_domain(self):
        with self.subTest():
            self.assertTrue(is_valid_full_duckdns_domain(TEST_DOMAIN))
            self.assertTrue(is_valid_full_duckdns_domain("test." + TEST_DOMAIN))
            self.assertTrue(is_valid_full_duckdns_domain("test.abc." + TEST_DOMAIN))
            self.assertTrue(is_valid_full_duckdns_domain("test.abc.efg." + TEST_DOMAIN))
            self.assertTrue(is_valid_full_duckdns_domain("test-abc." + TEST_DOMAIN))
            self.assertTrue(
                is_valid_full_duckdns_domain("test-abc.test-def." + TEST_DOMAIN)
            )

        with self.subTest():
            self.assertFalse(is_valid_full_duckdns_domain("abc.def.ghi"))
            self.assertFalse(is_valid_full_duckdns_domain("example.com"))
            self.assertFalse(is_valid_full_duckdns_domain("example.com."))
            self.assertFalse(is_valid_full_duckdns_domain("test.duckduckduck.org"))
            self.assertFalse(is_valid_full_duckdns_domain("test.duckdns.com"))


if __name__ == "__main__":
    unittest.main()
