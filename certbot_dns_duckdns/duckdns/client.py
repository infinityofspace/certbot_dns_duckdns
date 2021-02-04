import json

import requests

BASE_URL = "https://www.duckdns.org/update"
DNS_RESOLVE_BASE_URL = "https://dns.google/resolve?type=TXT"


class TXTUpdateError(Exception):
    pass


class DuckDNSClient:

    def __init__(self, token):
        self.token = token

    def set_txt_record(self, domain, txt):
        assert self.token is not None and len(self.token) > 0
        assert domain is not None and len(domain) > 0

        domain = domain.replace(".duckdns.org", "")

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

    def clear_txt_record(self, domain):
        assert self.token is not None and len(self.token) > 0
        assert domain is not None and len(domain) > 0

        domain = domain.replace(".duckdns.org", "")

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

    def get_txt_record(self, domain):
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
