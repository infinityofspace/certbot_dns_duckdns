"""
This module provides a client for clearing, setting and receiving the TXT record for DuckDNS domains.
"""

import logging
import re

import requests

# prevent urllib3 to log request with the api token
logging.getLogger("urllib3").setLevel(logging.WARNING)

BASE_URL = "https://www.duckdns.org/update"
VALID_DUCKDNS_DOMAIN_REGEX = re.compile(
    r"^([a-z\d\\-]+\.)*[a-z\d\\-]+(\.duckdns\.org)?$"
)
VALID_FULL_DUCKDNS_DOMAIN_REGEX = re.compile(
    r"^([a-z\d\\-]+\.)*[a-z\d\\-]+\.duckdns\.org$"
)


def is_valid_duckdns_domain(domain):
    """
    Check if the domain is a valid duckdns subdomain.

    :param domain: the domain to check

    :return: True if the domain is a valid duckdns subdomain, otherwise False
    """

    return VALID_DUCKDNS_DOMAIN_REGEX.match(domain) is not None


def is_valid_full_duckdns_domain(domain):
    """
    Check if the domain is a valid duckdns domain with the '.duckdns.org' suffix.

    :param domain: the domain to check

    :return: True if the domain is a valid duckdns domain, otherwise False
    """

    return VALID_FULL_DUCKDNS_DOMAIN_REGEX.match(domain) is not None


class TXTUpdateError(Exception):
    """
    Exception if during the TXT record changing something goes wrong.
    """

    template_txt_set = (
        'The TXT update "{txt}" for domain "{domain}" could not be set.\n'
        "Request status code: {status_code}\n"
        "Request response text: {response}"
    )

    template_txt_delete = (
        'The TXT value for domain "{domain}" could not be deleted.\n'
        "Request status code: {status_code}\n"
        "Request response text: {response}"
    )

    def __init__(self, domain, status_code, response, txt=None):
        self.txt = txt
        self.domain = domain
        self.status_code = status_code
        self.response = response

        if txt:
            self.message = self.template_txt_set.format(
                domain=domain, status_code=status_code, response=response, txt=txt
            )
        else:
            self.message = self.template_txt_delete.format(
                domain=domain, status_code=status_code, response=response
            )

        super().__init__(self.message)


class NotValidDuckdnsDomainError(Exception):
    """
    Exception if the domain is not a valid duckdns domain.
    """

    def __init__(self, domain):
        self.domain = domain
        self.message = f'The domain "{domain}" is not valid a duckdns subdomain.'
        super().__init__(self.message)


class NotValidDuckdnsTokenError(Exception):
    """
    Exception if the token is not a valid duckdns token.
    """

    def __init__(self):
        super().__init__("The token is not valid a duckdns token.")


class DuckDNSClient:
    """
    Client for clearing, setting and receiving the TXT record for DuckDNS domains.
    """

    def __init__(self, token: str) -> None:
        """
        Creates a new DuckDNSClient object.

        :param token: the DuckDNS token used for API calls

        :raise NotValidDuckdnsTokenError: if the token is not a valid duckdns token
        """
        if token is None or len(token) == 0:
            raise NotValidDuckdnsTokenError()

        self._token = token

    def set_txt_record(self, domain: str, txt: str, timeout: int = 600) -> None:
        """
        Set a TXT record value for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the value of the TXT entry should set
        :param txt: the string value to set as TXT record
        :param timeout: the timeout for the request in seconds

        :raise TXTUpdateError: if the TXT record can not be set
        :raise NotValidDuckdnsDomainError: if the domain is not a valid duckdns domain
        """

        if domain is None or not is_valid_duckdns_domain(domain):
            raise NotValidDuckdnsDomainError(domain)

        root_domain = self.__get_validated_root_domain__(domain)

        params = {"token": self._token, "domains": root_domain, "txt": txt}
        r = requests.get(url=BASE_URL, params=params, timeout=timeout)

        if r.text != "OK":
            raise TXTUpdateError(txt, domain, r.status_code, r.text)

    @staticmethod
    def __get_validated_root_domain__(domain):
        """
        Get the root domain from a DuckDNS domain.

        :param domain: only the subdomain of duckdns
        :return: the root domain

        :raise NotValidDuckdnsDomainError: if the domain is not a valid duckdns domain
        """
        # get the root domain with the first subdomain
        domain_parts = domain.split(".")
        root_domain = ".".join(domain_parts[-3:])
        if not is_valid_duckdns_domain(root_domain):
            raise NotValidDuckdnsDomainError(root_domain)

        return root_domain

    def clear_txt_record(self, domain: str, timeout: int = 600) -> None:
        """
        Clear the TXT record for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the TXT entry should be cleared
        :param timeout: the timeout for the request in seconds

        :raise TXTUpdateError: if the TXT record can not be cleared
        :raise NotValidDuckdnsDomainError: if the domain is not a valid duckdns domain
        """

        if domain is None or not is_valid_duckdns_domain(domain):
            raise NotValidDuckdnsDomainError(domain)

        root_domain = self.__get_validated_root_domain__(domain)

        params = {
            "token": self._token,
            "domains": root_domain,
            "txt": "",
            "clear": "true",
        }
        r = requests.get(url=BASE_URL, params=params, timeout=timeout)

        if r.text != "OK":
            raise TXTUpdateError(domain, r.status_code, r.text, None)
