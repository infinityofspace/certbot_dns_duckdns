import logging
import re

import requests

# prevent urllib3 to log request with the api token
logging.getLogger("urllib3").setLevel(logging.WARNING)

BASE_URL = "https://www.duckdns.org/update"
VALID_DUCKDNS_DOMAIN_REGEX = re.compile("^[a-z0-9\\-]+(.duckdns.org)?$")


class TXTUpdateError(Exception):
    """
    Exception if during the the TXT record changing something goes wrong.
    """
    pass


class DuckDNSClient:
    """
    Client for clearing, setting and receiving the TXT record for DuckDNS domains.
    """

    def __init__(self, token: str) -> None:
        """
        Creates a new DuckDNSClient object.

        :param token: the DuckDNS token used for API calls
        """

        self.token = token

    def set_txt_record(self, domain: str, txt: str) -> None:
        """
        Set a TXT record value for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the value of the TXT entry should set
        :param txt: the string value to set as TXT record
        :raise TXTUpdateError: if the TXT record can not be set
        """

        assert self.token is not None and len(self.token) > 0
        assert domain is not None and len(domain) > 0

        root_domain = self.__get_validated_root_domain__(domain)

        params = {
            "token": self.token,
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
        # get the root domain with the first subdomain
        domain_parts = domain.split(".")
        root_domain = ".".join(domain_parts[-3:])
        assert VALID_DUCKDNS_DOMAIN_REGEX.match(root_domain)

        return root_domain

    def clear_txt_record(self, domain: str) -> None:
        """
        Clear the TXT record for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the TXT entry should be cleared
        :raise TXTUpdateError: if the TXT record can not be cleared
        """

        assert self.token is not None and len(self.token) > 0
        assert domain is not None and len(domain) > 0

        root_domain = self.__get_validated_root_domain__(domain)

        params = {
            "token": self.token,
            "domains": root_domain,
            "txt": "",
            "clear": "true"
        }
        r = requests.get(url=BASE_URL, params=params)

        if r.text != "OK":
            raise TXTUpdateError("The clearing of the TXT record for domain \"{}\" was not successful.\n"
                                 "Request status code: {}\n"
                                 "Request response text: {}".format(domain, r.status_code, r.text))
