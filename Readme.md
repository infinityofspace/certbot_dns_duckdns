# Certbot DNS DuckDNS Plugin

Plugin for certbot for a DNS-01 challenge with a DuckDNS domain.

---

![PyPI](https://img.shields.io/pypi/v/certbot_dns_duckdns) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/certbot_dns_duckdns) [![GitHub](https://img.shields.io/github/license/infinityofspace/certbot_dns_duckdns)](https://github.com/infinityofspace/certbot_dns_duckdns/blob/master/License) ![PyPI - Downloads](https://img.shields.io/pypi/dm/certbot_dns_duckdns)

---

### Table of Contents

1. [About](#about)
2. [Installation](#installation)
    1. [Prerequirements](#prerequirements)
    2. [With pip (recommend)](#with-pip-recommend)
    3. [From source](#from-source)
    4. [Docker installation](#docker-installation)
3. [Usage](#usage)
    1. [Local installation usage](#local-installation-usage)
    2. [Docker usage](#docker-usage)
4. [Third party notices](#third-party-notices)
5. [License](#license)

---

### About

*certbot_dn_duckdns* is a plugin for [*certbot*](https://github.com/certbot/certbot) to create the DNS-01 challenge for
a DuckDNS domain. The plugin takes care of setting and deleting the TXT entry via the DuckDNS API.

### Installation

#### Prerequirements

*If you want to use the docker image, then you don't need any requirements other than a docker installation and can
proceed directly to the [installation](#docker-installation)*

You need at least version 3.6 of Python installed. If you want to install this plugin with pip, then you also need pip3
installed.

If you already have *certbot* installed, make sure you have at least version 1.1.0 installed.

You can check what version of *certbot* is installed with this command:

```commandline
certbot --version
```

If you don't have certbot installed yet, then the PyPI version of certbot will be installed automatically during the
installation.

**Note: If you want to run certbot with root privileges, then you need to install the plugin with root privileges too.
Otherwise certbot cannot find the plugin.**

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

#### Docker installation

You can also simply use the plugin with docker. You just have to clone the project with git first:

```commandline
git clone https://github.com/infinityofspace/certbot_dns_duckdns
```

Now build a local Docker image:

```commandline
cd certbot_dns_duckdns
docker build -t certbot_dns_duckdns:v0.3 .
```

You are now done and can proceed to the [usage description](#docker-usage) of the plugin with docker.

### Usage

#### Local installation usage

To check if the plugin is installed correctly and detected properly by certbot, you can use the following command:

```commandline
certbot plugins
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

You can find al list of all available certbot cli options in
the [official documentation](https://certbot.eff.org/docs/using.html#certbot-command-line-options) of *certbot*.

#### Docker usage

Please make sure that you have completed [the installation](#installation).

You can start the container to obtain a new certificate:

```commandline
docker run \
-e DOMAIN="<your-full-duckdns-domain>" \
-e EMAIL="<your-email>" \
-e DUCKDNS_TOKEN="<your-duckdns-token>" \
certbot_dns_duckdns:v0.3
```

You have the following options

| environment variable | description | required |
|:--------------------:|:-----------:|:--------:|
| DOMAIN | The DuckDNS domain for which you want to get the certificate | yes |
| DUCKDNS_TOKEN | Your DuckDNS API Token | yes |
| EMAIL | Your email address with which the Letsencrypt account should be created.<br>If it is not specified, then no account will be created.  | no |
| STAGING | Use the staging environment of Letsencrypt. Default value is false | no |
| AUTORENEW | Renew the certificate automatically. Default value is false | no |
| RECREATE | Delete all previous certificate data data. Default value is false | no |
| ADDITIONAL_CERTBOT_ARGS | A string with additional certbot arguments.<br>For example: "--deploy-hook ./hooks/my_cert_hook.sh" | no |

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
