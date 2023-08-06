# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

import pytest

from libwebid.lib import email


@pytest.mark.asyncio
@pytest.mark.parametrize("value,result", [
    ("user@unimatrixone.io", True),
    ("user@webidentity.id", True),
    (f"user@{secrets.token_hex(16)}.com", False),
    (f"user@webidentityapis.com", False),
])
async def test_can_login_with_google(value: str, result: str):
    assert await email.can_login_with_google(value) == result


@pytest.mark.asyncio
@pytest.mark.parametrize("value,result", [
    (["unimatrixone.io", "webidentity.id"], {"google-workspace"}),
    ([f"{secrets.token_hex(16)}.id"], set()),
])
async def test_get_domain_email_verification_methods(
    value: list[str],
    result: set[str]
):
    assert await email.get_domain_email_verification_methods(value) == result