import os
import time
import unittest

from dns import resolver
from dns.resolver import Resolver

from certbot_dns_duckdns.cert.client import DEFAULT_PROPAGATION_SECONDS
from certbot_dns_duckdns.duckdns.client import DuckDNSClient, TXTUpdateError, NotValidDuckdnsTokenError, \
    NotValidDuckdnsDomainError, is_valid_duckdns_domain, is_valid_full_duckdns_domain

TEST_DOMAIN = os.environ.get("TEST_DOMAIN")
TEST_DUCKDNS_TOKEN = os.environ.get("TEST_DUCKDNS_TOKEN")

NAMESERVER = ["1.1.1.1"]

assert TEST_DOMAIN is not None and len(TEST_DOMAIN) > 0
assert TEST_DUCKDNS_TOKEN is not None and len(TEST_DUCKDNS_TOKEN) > 0


class DuckDNSTests(unittest.TestCase):

    def test_invalid_token(self):
        duckdns_client = DuckDNSClient("42")

        with self.subTest():
            # test set txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.set_txt_record(TEST_DOMAIN, "simple text")

        with self.subTest():
            # test clear txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.clear_txt_record(TEST_DOMAIN)

    def test_empty_token(self):
        with self.subTest():
            with self.assertRaises(NotValidDuckdnsTokenError):
                duckdns_client = DuckDNSClient("")

        # explicitly set the token to an empty string
        duckdns_client = DuckDNSClient("test")
        duckdns_client._token = ""

        with self.subTest():
            # test set txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.set_txt_record(TEST_DOMAIN, "simple text")

        with self.subTest():
            # test clear txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.clear_txt_record(TEST_DOMAIN)

    def test_none_token(self):
        with self.subTest():
            with self.assertRaises(NotValidDuckdnsTokenError):
                duckdns_client = DuckDNSClient(None)

        # explicitly set the token to None
        duckdns_client = DuckDNSClient("test")
        duckdns_client._token = None

        with self.subTest():
            # test set txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.set_txt_record(TEST_DOMAIN, "simple text")

        with self.subTest():
            # test clear txt record
            with self.assertRaises(TXTUpdateError):
                duckdns_client.clear_txt_record(TEST_DOMAIN)

    def test_wrong_domain(self):
        duckdns_client = DuckDNSClient(TEST_DUCKDNS_TOKEN)

        with self.subTest():
            with self.assertRaises(TXTUpdateError):
                duckdns_client.set_txt_record("thisdomainsiswrong", "simple text")

        with self.subTest():
            with self.assertRaises(TXTUpdateError):
                duckdns_client.clear_txt_record("thisdomainsiswrong")

    def test_empty_domain(self):
        duckdns_client = DuckDNSClient(TEST_DUCKDNS_TOKEN)

        with self.subTest():
            with self.assertRaises(NotValidDuckdnsDomainError):
                duckdns_client.set_txt_record("", "simple text")

        with self.subTest():
            with self.assertRaises(NotValidDuckdnsDomainError):
                duckdns_client.clear_txt_record("")

    def test_add_txt(self):
        txt_record_text = "simple text"

        duckdns_client = DuckDNSClient(TEST_DUCKDNS_TOKEN)

        duckdns_client.set_txt_record(TEST_DOMAIN, txt_record_text)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)
        # get the set txt record from the specified nameserver
        custom_resolver = Resolver()
        custom_resolver.nameservers = NAMESERVER
        txt_value = custom_resolver.resolve(TEST_DOMAIN, "TXT").response.answer[0][0].strings[0].decode("utf-8")

        self.assertEqual(txt_record_text, txt_value)

    def test_get_validated_root_domain_hyphen_domain(self):
        domain = "test-example.duckdns.org"
        root_domain = DuckDNSClient.__get_validated_root_domain__(domain)
        self.assertEqual(root_domain, domain)

    def test_get_validated_root_domain_multiple_subdomains(self):
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("test1.test2." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("test1.test2.test3." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)

    def test_get_validated_root_domain_special_subdomains(self):
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("test-." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("test--." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("-test." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("--test." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("-." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("--." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("-test-." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("test--test." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("12345." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("12345-." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("12345--." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("-12345." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("--12345." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)
        with self.subTest():
            root_domain = DuckDNSClient.__get_validated_root_domain__("-123ad-sdas--45-as-." + TEST_DOMAIN)
            self.assertEqual(root_domain, TEST_DOMAIN)

    def test_clear_txt(self):
        duckdns_client = DuckDNSClient(TEST_DUCKDNS_TOKEN)

        txt_record_text = "simple text"
        duckdns_client.set_txt_record(TEST_DOMAIN, txt_record_text)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)

        duckdns_client.clear_txt_record(TEST_DOMAIN)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)

        # get the cleared txt record from the specified nameserver
        custom_resolver = resolver.Resolver()
        custom_resolver.nameservers = NAMESERVER

        txt_value = custom_resolver.resolve(TEST_DOMAIN, "TXT").response.answer[0][0].strings[0].decode("utf-8")

        self.assertEqual("", txt_value)

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
            self.assertTrue(is_valid_full_duckdns_domain("test-abc.test-def." + TEST_DOMAIN))

        with self.subTest():
            self.assertFalse(is_valid_full_duckdns_domain("abc.def.ghi"))
            self.assertFalse(is_valid_full_duckdns_domain("example.com"))
            self.assertFalse(is_valid_full_duckdns_domain("example.com."))
            self.assertFalse(is_valid_full_duckdns_domain("test.duckduckduck.org"))
            self.assertFalse(is_valid_full_duckdns_domain("test.duckdns.com"))


if __name__ == "__main__":
    unittest.main()
