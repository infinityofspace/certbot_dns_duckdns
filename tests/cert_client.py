import unittest
from argparse import Namespace

import responses
from certbot.configuration import NamespaceConfig
from certbot.errors import PluginError

from certbot_dns_duckdns.cert.client import Authenticator


class TestCertClient(unittest.TestCase):
    @responses.activate
    def test_valid_auth(self):
        api_token = "token"
        domain = "example.duckdns.org"
        txt_value = "ABCDEF"

        responses.get(
            url=f"https://www.duckdns.org/update?token={api_token}&domains={domain}&txt={txt_value}",
            body="OK",
        )

        namespace = Namespace(
            duckdns_token=api_token,
            duckdns_token_token_env="DUCKDNS_TOKEN",
            duckdns_no_txt_restore=False,
            config_dir="config_dir",
            work_dir="work_dir",
            logs_dir="logs_dir",
            http01_port=80,
            https_port=443,
            domains=["example.duckdns.org"],
        )
        config = NamespaceConfig(namespace)

        authenticator = Authenticator(config, name="duckdns")

        authenticator._perform(domain=domain, validation_name="", validation=txt_value)

    @responses.activate
    def test_invalid_auth(self):
        api_token = "token"
        domain = "example.duckdns.org"
        txt_value = "ABCDEF"

        responses.get(
            url=f"https://www.duckdns.org/update?token={api_token}&domains={domain}&txt={txt_value}",
            body="OK",
        )

        namespace = Namespace(
            duckdns_token=api_token + "invalid",
            duckdns_token_token_env="DUCKDNS_TOKEN",
            duckdns_no_txt_restore=False,
            config_dir="config_dir",
            work_dir="work_dir",
            logs_dir="logs_dir",
            http01_port=80,
            https_port=443,
            domains=["example.duckdns.org"],
        )
        config = NamespaceConfig(namespace)

        authenticator = Authenticator(config, name="duckdns")

        with self.assertRaises(PluginError):
            authenticator._perform(
                domain=domain, validation_name="", validation=txt_value
            )

    @responses.activate
    def test_invalid_duckdns_domain(self):
        api_token = "token"
        domain = "example.org"
        txt_value = "ABCDEF"

        responses.get(
            url=f"https://www.duckdns.org/update?token={api_token}&domains={domain}&txt={txt_value}",
            body="OK",
        )

        namespace = Namespace(
            duckdns_token=api_token,
            duckdns_token_token_env="DUCKDNS_TOKEN",
            duckdns_no_txt_restore=False,
            config_dir="config_dir",
            work_dir="work_dir",
            logs_dir="logs_dir",
            http01_port=80,
            https_port=443,
            domains=[domain],
        )
        config = NamespaceConfig(namespace)

        authenticator = Authenticator(config, name="duckdns")

        with self.assertRaises(PluginError):
            authenticator._perform(
                domain=domain, validation_name="", validation=txt_value
            )

    @responses.activate
    def test_cleanup(self):
        api_token = "token"
        domain = "example.duckdns.org"
        txt_value = "ABCDEF"

        responses.get(
            url=f"https://www.duckdns.org/update?token={api_token}&domains={domain}&txt=&clear=true",
            body="OK",
        )

        namespace = Namespace(
            duckdns_token=api_token,
            duckdns_token_token_env="DUCKDNS_TOKEN",
            duckdns_no_txt_restore=False,
            config_dir="config_dir",
            work_dir="work_dir",
            logs_dir="logs_dir",
            http01_port=80,
            https_port=443,
            domains=["example.duckdns.org"],
        )
        config = NamespaceConfig(namespace)

        authenticator = Authenticator(config, name="duckdns")

        authenticator._cleanup(domain=domain, validation_name="", validation=txt_value)
