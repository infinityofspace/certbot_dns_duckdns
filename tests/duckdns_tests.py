import os
import time
import unittest

from certbot_dns_duckdns.cert.client import DEFAULT_PROPAGATION_SECONDS
from certbot_dns_duckdns.duckdns.client import DuckDNSClient, TXTUpdateError

DOMAIN = os.environ.get("TEST_DOMAIN")
DUCKDNS_TOKEN = os.environ.get("TEST_DUCKDNS_TOKEN")


class DuckDNSTests(unittest.TestCase):

    def test_invalid_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient("42")

        # test set txt record
        txt_set_error = False
        try:
            duckdns_client.set_txt_record(DOMAIN, "simple text")
        except TXTUpdateError:
            txt_set_error = True
        self.assertEqual(True, txt_set_error)

        # test clear txt record
        txt_clear_error = False
        try:
            duckdns_client.clear_txt_record(DOMAIN)
        except TXTUpdateError:
            txt_clear_error = True
        self.assertEqual(True, txt_clear_error)

    def test_empty_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient("")

        # test set txt record
        txt_set_error = False
        try:
            duckdns_client.set_txt_record(DOMAIN, "simple text")
        except AssertionError:
            txt_set_error = True
        self.assertEqual(True, txt_set_error)

        # test clear txt record
        txt_clear_error = False
        try:
            duckdns_client.clear_txt_record(DOMAIN)
        except AssertionError:
            txt_clear_error = True
        self.assertEqual(True, txt_clear_error)

    def test_none_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient(None)

        # test set txt record
        txt_set_error = False
        try:
            duckdns_client.set_txt_record(DOMAIN, "simple text")
        except AssertionError:
            txt_set_error = True
        self.assertEqual(True, txt_set_error)

        # test clear txt record
        txt_clear_error = False
        try:
            duckdns_client.clear_txt_record(DOMAIN)
        except AssertionError:
            txt_clear_error = True
        self.assertEqual(True, txt_clear_error)

    def test_invalid_domain(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient(DUCKDNS_TOKEN)

        with self.assertRaises(TXTUpdateError):
            duckdns_client.set_txt_record("thisdomainsisnotvalid", "simple text")

        with self.assertRaises(TXTUpdateError):
            duckdns_client.clear_txt_record("thisdomainsisnotvalid")

    def test_empty_domain(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient(DUCKDNS_TOKEN)

        with self.assertRaises(AssertionError):
            duckdns_client.set_txt_record("", "simple text")

        with self.assertRaises(AssertionError):
            duckdns_client.clear_txt_record("")

    def test_add_txt(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient(DUCKDNS_TOKEN)

        txt_record_text = "simple text"
        duckdns_client.set_txt_record(DOMAIN, txt_record_text)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)
        txt_value = duckdns_client.get_txt_record(DOMAIN)

        self.assertEqual(txt_record_text, txt_value)

    def test_clear_txt(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        duckdns_client = DuckDNSClient(DUCKDNS_TOKEN)

        txt_record_text = "simple text"
        duckdns_client.set_txt_record(DOMAIN, txt_record_text)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)
        duckdns_client.get_txt_record(DOMAIN)

        duckdns_client.clear_txt_record(DOMAIN)
        # wait sometime for propagation of the txt update
        print("wait for the txt record update to propagate...")
        time.sleep(DEFAULT_PROPAGATION_SECONDS)
        txt_value = duckdns_client.get_txt_record(DOMAIN)

        self.assertEqual("", txt_value)


if __name__ == "__main__":
    unittest.main()
