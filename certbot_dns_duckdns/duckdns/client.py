import logging
import re

import requests

# prevent urllib3 to log request with the api token
logging.getLogger("urllib3").setLevel(logging.WARNING)

BASE_URL = "https://www.duckdns.org/update"
VALID_DUCKDNS_DOMAIN_REGEX = re.compile(r"^([a-z\d\\-]+\.)*[a-z\d\\-]+(\.duckdns\.org)?$")
VALID_FULL_DUCKDNS_DOMAIN_REGEX = re.compile(r"^([a-z\d\\-]+\.)*[a-z\d\\-]+\.duckdns\.org$")


def is_valid_duckdns_domain(domain):
    return VALID_DUCKDNS_DOMAIN_REGEX.match(domain) is not None


def is_valid_full_duckdns_domain(domain):
    return VALID_FULL_DUCKDNS_DOMAIN_REGEX.match(domain) is not None


class TXTUpdateError(Exception):
    """
    Exception if during the TXT record changing something goes wrong.
    """
    pass


class NotValidDuckdnsDomainError(Exception):
    """
    Exception if the domain is not a valid duckdns domain.
    """

    def __init__(self, domain):
        self.domain = domain
        self.message = f"The domain \"{domain}\" is not valid a duckdns subdomain."
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

    def set_txt_record(self, domain: str, txt: str) -> None:
        """
        Set a TXT record value for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the value of the TXT entry should set
        :param txt: the string value to set as TXT record

        :raise TXTUpdateError: if the TXT record can not be set
        :raise NotValidDuckdnsDomainError: if the domain is not a valid duckdns domain
        """

        if domain is None or not is_valid_duckdns_domain(domain):
            raise NotValidDuckdnsDomainError(domain)

        root_domain = self.__get_validated_root_domain__(domain)

        params = {
            "token": self._token,
            "domains": root_domain,
            "txt": txt
        }
        r = requests.get(url=BASE_URL, params=params)

        if r.text != "OK":
            raise TXTUpdateError("The TXT update \"{}\" for domain \"{}\" could not be set.\n"
                                 "Request status code: {}\n"
                                 "Request response text: {}".format(txt, domain, r.status_code, r.text))

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

    def clear_txt_record(self, domain: str) -> None:
        """
        Clear the TXT record for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the TXT entry should be cleared

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
            "clear": "true"
        }
        r = requests.get(url=BASE_URL, params=params)

        if r.text != "OK":
            raise TXTUpdateError("The clearing of the TXT record for domain \"{}\" was not successful.\n"
                                 "Request status code: {}\n"
                                 "Request response text: {}".format(domain, r.status_code, r.text))
