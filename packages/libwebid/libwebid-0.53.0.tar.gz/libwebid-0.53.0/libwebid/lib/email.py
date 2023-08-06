# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import re

from dns.resolver import NXDOMAIN
from dns.resolver import NoAnswer
from dns.asyncresolver import Resolver


resolver: Resolver = Resolver()
resolver.nameservers = ["8.8.8.8"]


def is_google_workspace(domain: str) -> bool:
    """Return a boolean indicating if the domain uses Google Workspace"""
    return re.match('^.*(l.google.com|googlemail.com)$', str.lower(domain)) is not None


async def get_mx_records(domain: str) -> set[str]:
    """Return the mailservers used by the given domain."""
    try:
        answer = await resolver.resolve(domain, rdtype='MX') # type: ignore
        return {str.strip(str(x.exchange), '.') for x in answer.rrset} # type: ignore
    except (NXDOMAIN, NoAnswer):
        return set()

async def can_login_with_google(email: str) -> bool:
    """Return a boolean indicating if the email address can login
    with Google.
    """
    _, domain = str.split(email, '@')
    return any([is_google_workspace(x) for x in await get_mx_records(domain)])


async def get_domain_email_verification_methods(domains: list[str]) -> set[str]:
    """Return a set containing the methods that may be used to verify
    that person has access to an email address with the given list of
    domains.
    """
    methods: set[str] = set()
    for records in await asyncio.gather(*[get_mx_records(x) for x in domains]):
        if any(is_google_workspace(x) for x in records):
            methods.add('google-workspace')
    return methods