# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from libwebid.lib import email


@pytest.mark.parametrize("value,result", [
    ('ASPMX.L.GOOGLE.COM', True),
    ('ALT1.ASPMX.L.GOOGLE.COM', True),
    ('ALT2.ASPMX.L.GOOGLE.COM', True),
    ('ALT3.ASPMX.L.GOOGLE.COM', True),
    ('ALT4.ASPMX.L.GOOGLE.COM', True),
    ('ASPMX.GOOGLEMAIL.COM', True),
    ('ASPMX2.GOOGLEMAIL.COM', True),
])
def test_domain_is_google_workspace(value: str, result: str):
    assert email.is_google_workspace(value) == result