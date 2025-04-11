from setuptools import setup, find_packages

from certbot_dns_duckdns import __version__

with open("Readme.md") as f:
    long_description = f.read()

setup(
    name="certbot_dns_duckdns",
    version=__version__,
    author="infinityofspace",
    url="https://github.com/infinityofspace/certbot_dns_duckdns",
    description="Obtain certificates using a DNS TXT record for DuckDNS domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
    ],
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.9",
    install_requires=[
        "certbot>=1.18.0,<5.0",
        "requests>=2.20.0,<3.0",
        "dnspython>=2.0.0,<3.0",
    ],
    entry_points={
        "certbot.plugins": [
            "dns-duckdns = certbot_dns_duckdns.cert.client:Authenticator",
        ]
    },
)
