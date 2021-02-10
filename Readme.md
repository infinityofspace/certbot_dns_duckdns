# Certbot DNS DuckDNS Plugin

Plugin for certbot for a DNS-01 challenge with a DuckDNS domain.

---

![PyPI](https://img.shields.io/pypi/v/certbot_dns_duckdns) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/certbot_dns_duckdns) [![GitHub](https://img.shields.io/github/license/infinityofspace/certbot_dns_duckdns)](https://github.com/infinityofspace/certbot_dns_duckdns/blob/master/License) ![PyPI - Downloads](https://img.shields.io/pypi/dm/certbot_dns_duckdns)

---

### Table of Contents

1. [About](#about)
2. [Installation](#installation)
    1. [With pip (recommend)](#with-pip-recommend)
    2. [From source](#from-source)
3. [Usage](#usage)
4. [Third party notices](#third-party-notices)
5. [License](#license)

---

### About

*certbot_dn_duckdns* is a plugin for [*certbot*](https://github.com/certbot/certbot) to create the DNS-01 challenge for
a DuckDNS domain. The plugin takes care of setting and deleting the TXT entry via the DuckDNS API.

### Installation

This project requires Python 3 to be installed.

#### With pip (recommend)

Use the following command to install *certbot_dns_duckdns* with pip:

```commandline
pip install certbot_dns_duckdns
```

You can also very easily update to a newer version:

```commandline
pip install certbot_dns_duckdns -U
```

#### From source

```commandline
git clone https://github.com/infinityofspace/certbot_dns_duckdns
cd certbot_dns_duckdns
pip install .
```

### Usage

Make sure before you start that you have a current version of *certbot* installed. You can read how to install *certbot*
in the [official documentation](https://certbot.eff.org/docs/install.html).

*Note: Normally, the PYPI version of *certbot* is installed with the installation of *certbot_dns_duckdns*
and does not require any further installation or configuration. However, you may need a customized installation for your
use case, check the official documentation for that*

You can check if *certbot* is installed with:

```commandline
certbot --version
```

---
Below are some examples of how to use the plugin:

Generate a certificate for a DNS-01 challenge of the domain "example.duckdns.org":

```commandline
certbot certonly \
  --non-interactive \
  --agree-tos \
  --email <your-email> \
  --preferred-challenges dns \
  --authenticator dns-duckdns \
  --dns-duckdns-token <your-duckdns-token> \
  --dns-duckdns-propagation-seconds 60 \
  -d "example.duckdns.org"
```

Generate a wildcard certificate for a DNS-01 challenge of all subdomains "*.example.duckdns.org":

```commandline
certbot certonly \
  --non-interactive \
  --agree-tos \
  --email <your-email> \
  --preferred-challenges dns \
  --authenticator dns-duckdns \
  --dns-duckdns-token <your-duckdns-token> \
  --dns-duckdns-propagation-seconds 60 \
  -d "*.example.duckdns.org"
```

Generate a certificate for a DNS-01 challenge of the domain "example.duckdns.org" without an account (i.e. without an
email address):

```commandline
certbot certonly \
  --non-interactive \
  --agree-tos \
  --register-unsafely-without-email \
  --preferred-challenges dns \
  --authenticator dns-duckdns \
  --dns-duckdns-token <your-duckdns-token> \
  --dns-duckdns-propagation-seconds 60 \
  -d "example.duckdns.org"
```

Generate a staging certificate (i.e. temporary testing certificate) for a DNS-01 challenge of the domain "
example.duckdns.org":

```commandline
certbot certonly \
  --non-interactive \
  --agree-tos \
  --email <your-email> \
  --preferred-challenges dns \
  --authenticator dns-duckdns \
  --dns-duckdns-token <your-duckdns-token> \
  --dns-duckdns-propagation-seconds 60 \
  -d "example.duckdns.org" \
  --staging
```

You can find al list of all available cli options in
the [official documentation](https://certbot.eff.org/docs/using.html#certbot-command-line-options) of *certbot*.

### Third party notices

All modules used by this project are listed below:

| Name | License|
|:---:|:---:|
| [certbot](https://github.com/certbot/certbot) | [Apache 2.0](https://raw.githubusercontent.com/certbot/certbot/master/LICENSE.txt) |
| [requests](https://github.com/psf/requests) | [Apache 2.0](https://raw.githubusercontent.com/psf/requests/master/LICENSE) |
| [zope.interface](https://github.com/zopefoundation/zope.interface) | [ZPL-2.1](https://raw.githubusercontent.com/zopefoundation/zope.interface/master/LICENSE.txt) |
| [setuptools](https://github.com/pypa/setuptools) | [MIT](https://raw.githubusercontent.com/pypa/setuptools/main/LICENSE) |

Furthermore, this readme file contains embeddings of [Shields.io](https://github.com/badges/shields).

### License

[MIT](https://github.com/infinityofspace/certbot_dns_duckdns/blob/master/License) - Copyright (c) 2021 Marvin Heptner
