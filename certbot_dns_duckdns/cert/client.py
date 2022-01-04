import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common
from dns import resolver

from certbot_dns_duckdns.duckdns.client import DuckDNSClient

DEFAULT_PROPAGATION_SECONDS = 30
TXT_MAX_LEN = 255


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """
    Authenticator class to handle dns-01 challenge for DuckDNS domains.
    """

    description = "Obtain certificates using a DNS TXT record for DuckDNS domains"
    old_txt_value = ""

    def __init__(self, *args, **kwargs) -> None:
        super(Authenticator, self).__init__(*args, **kwargs)

    @classmethod
    def add_parser_arguments(cls, add: callable) -> None:
        """
        Add required or optional argument for the cli of certbot.

        :param add: method handling the argument adding to the cli
        """

        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=DEFAULT_PROPAGATION_SECONDS)
        add("credentials", help="DuckDNS credentials INI file.")
        add("token", help="DuckDNS token (overwrites credentials file)")
        add("no-txt-restore",
            default=False,
            action="store_true",
            help="Do not restore the original TXT record")

    def more_info(self) -> str:
        """
        Get more information about this plugin.
        This method is used by certbot to show more info about this plugin.

        :return: string with more information about this plugin
        """
        return "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using the DuckDNS API."

    def _setup_credentials(self) -> None:
        # If token cli param is provided we do not need a credentials file
        if self.conf("token"):
            return

        self._configure_file('credentials',
                             'DuckDNS credentials INI file')
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            "credentials",
            "DuckDNS credentials INI file",
            {
                "token": "DuckDNS token",
            },
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Add the TXT record of the provided DuckDNS domain.

        :param domain: the DuckDNS domain
        :param validation_name: value to validate the dns challenge
        :param validation: the value for the TXT record
        :raise PluginError: if the TXT record can not be set of something goes wrong
        """

        if not self.conf("no-txt-restore"):
            # get the current TXT record
            custom_resolver = resolver.Resolver()
            try:
                txt_values = custom_resolver.resolve(domain, "TXT")
            except Exception as e:
                raise errors.PluginError(e)

            # there should only be one single TXT record
            if len(txt_values) != 1:
                raise errors.PluginError("issue resoling TXT record")

            # remove the additional quotes around the TXT value
            self.old_txt_value = txt_values[0].to_text()[1:-1]

        try:
            self._get_duckdns_client().set_txt_record(domain, validation)
        except Exception as e:
            raise errors.PluginError(e)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Clear the dns validation from the TXT record of the provided DuckDNS domain. Restore the previous TXT value if
        the TXT value was not empty before the DNS challenge.

        :param domain: the DuckDNS domain
        :param validation_name: value to validate the dns challenge
        :param validation: the value for the TXT record
        :raise PluginError:  if the TXT record can not be cleared of something goes wrong
        """

        try:
            if self.old_txt_value == "":
                # setting an empty TXT value does not work with the DuckDNS API
                self._get_duckdns_client().clear_txt_record(domain)
            else:
                self._get_duckdns_client().set_txt_record(domain, self.old_txt_value)
        except Exception as e:
            raise errors.PluginError(e)

    def _get_duckdns_client(self) -> DuckDNSClient:
        """
        Create a new DuckDNSClient with the provided API token.

        :return: the created DuckDNSClient object
        """
        token = self.conf("token") or self.credentials.conf("token")
        return DuckDNSClient(token)
