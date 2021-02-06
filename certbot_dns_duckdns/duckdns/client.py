import json
import re
from typing import Optional

import requests

BASE_URL = "https://www.duckdns.org/update"
DNS_RESOLVE_BASE_URL = "https://dns.google/resolve?type=TXT"
VALID_DUCKDNS_DOMAIN_REGEX = re.compile("^[a-z0-9]+(.duckdns.org)?$")


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

        # remove any wildcard in the domain, because the DuckDNS API does not support wildcard
        domain = domain.replace("*.", "")

        assert VALID_DUCKDNS_DOMAIN_REGEX.match(domain)

        params = {
            "token": self.token,
            "domains": domain,
            "txt": txt
        }
        r = requests.get(url=BASE_URL, params=params)

        if r.text != "OK":
            raise TXTUpdateError("The TXT update \"{}\" for domain \"{}\" could not be set.\n"
                                 "Request status code: {}\n"
                                 "Request response text: {}".format(txt, domain, r.status_code, r.text))

    def clear_txt_record(self, domain: str) -> None:
        """
        Clear the TXT record for a specific DuckDNS domain.

        :param domain: the full domain or only the subdomain of duckdns
            (e.g. example of the full domain example.duckdns.org) for which the TXT entry should be cleared
        :raise TXTUpdateError: if the TXT record can not be cleared
        """

        assert self.token is not None and len(self.token) > 0
        assert domain is not None and len(domain) > 0

        # remove any wildcard in the domain, because the DuckDNS API does not support wildcard
        domain = domain.replace("*.", "")

        assert VALID_DUCKDNS_DOMAIN_REGEX.match(domain)

        params = {
            "token": self.token,
            "domains": domain,
            "txt": "",
            "clear": "true"
        }
        r = requests.get(url=BASE_URL, params=params)

        if r.text != "OK":
            raise TXTUpdateError("The clearing of the TXT record for domain \"{}\" was not successful.\n"
                                 "Request status code: {}\n"
                                 "Request response text: {}".format(domain, r.status_code, r.text))

    def get_txt_record(self, domain: str) -> Optional[str]:
        """
        Get the TXT record for a specific domain from the Google DNS Resolver API.

        :param domain: the full domain for which the TXT entry should be retrieved
        :return: the TXT record data or None if there is no such value
        """

        assert domain is not None and len(domain) > 0

        # remove any wildcard in the domain
        domain = domain.replace("*.", "")

        assert VALID_DUCKDNS_DOMAIN_REGEX.match(domain)

        params = {
            "name": domain
        }
        r = requests.get(url=DNS_RESOLVE_BASE_URL, params=params)

        res_json = json.loads(r.text)
        answer = res_json.get("Answer", None)
        if answer is not None and isinstance(answer, list) and len(answer) > 0:
            txt = answer[0].get("data", None)
            if txt is not None:
                # remove the quotation marks from the txt value
                return txt.replace("\"", "")
