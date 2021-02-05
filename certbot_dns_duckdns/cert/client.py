import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common

from certbot_dns_duckdns.duckdns.client import DuckDNSClient

DEFAULT_PROPAGATION_SECONDS = 30


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """
    Authenticator class to handle dns-01 challenge for DuckDNS domains.
    """

    description = "Obtain certificates using a DNS TXT record for DuckDNS domains"

    def __init__(self, *args, **kwargs) -> None:
        super(Authenticator, self).__init__(*args, **kwargs)

    @classmethod
    def add_parser_arguments(cls, add: callable) -> None:
        """
        Add required or optional argument for the cli of certbot.

        :param add: method handling the argument adding to the cli
        """

        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=DEFAULT_PROPAGATION_SECONDS)
        add("token", help="DuckDNS token")

    def more_info(self) -> str:
        """
        Get more information about this plugin.
        This method is used by certbot to show more info about this plugin.

        :return: string with more information about this plugin
        """
        return "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using the DuckDNS API."

    def _setup_credentials(self):
        pass

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Add the TXT record of the provided DuckDNS domain.

        :param domain: the DuckDNS domain
        :param validation_name: value to validate the dns challenge
        :param validation: the value for the TXT record
        :raise PluginError: if the TXT record can not be set of something goes wrong
        """

        try:
            self._get_duckdns_client().set_txt_record(domain, validation)
        except Exception as e:
            raise errors.PluginError(e)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Clear the TXT record of the provided DuckDNS domain.

        :param domain: the DuckDNS domain
        :param validation_name: value to validate the dns challenge
        :param validation: the value for the TXT record
        :raise PluginError:  if the TXT record can not be cleared of something goes wrong
        """

        try:
            self._get_duckdns_client().clear_txt_record(domain)
        except Exception as e:
            raise errors.PluginError(e)

    def _get_duckdns_client(self) -> DuckDNSClient:
        """
        Create a new DuckDNSClient with the provided API token.

        :return: the created DuckDNSClient object
        """

        return DuckDNSClient(self.conf("token"))
