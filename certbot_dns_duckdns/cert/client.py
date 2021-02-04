import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common

from certbot_dns_duckdns.duckdns.client import DuckDNSClient

DEFAULT_PROPAGATION_SECONDS = 30


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    description = "Obtain certificates using a DNS TXT record for DuckDNS domains"

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=DEFAULT_PROPAGATION_SECONDS)
        add("token", help="DuckDNS token")

    def more_info(self):
        return "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using the DuckDNS API."

    def _setup_credentials(self):
        pass

    def _perform(self, domain, validation_name, validation):
        try:
            self._get_duckdns_client().set_txt_record(domain, validation)
        except Exception as e:
            raise errors.PluginError(e)

    def _cleanup(self, domain, validation_name, validation):
        try:
            self._get_duckdns_client().clear_txt_record(domain)
        except Exception as e:
            raise errors.PluginError(e)

    def _get_duckdns_client(self):
        return DuckDNSClient(self.conf("token"))
