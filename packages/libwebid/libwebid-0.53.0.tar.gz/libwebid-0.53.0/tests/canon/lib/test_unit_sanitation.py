# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from libwebid.lib import sanitation


@pytest.mark.parametrize("value,result", [
    ("cochiseruhulessin@gmail.com", "cochiseruhulessin@gmail.com"),
    ("cochise.ruhulessin@gmail.com", "cochiseruhulessin@gmail.com"),
    ("cochiseruhulessin+foo@gmail.com", "cochiseruhulessin@gmail.com"),
    ("cochise.ruhulessin+foo@gmail.com", "cochiseruhulessin@gmail.com"),
    ("Cochise.ruhulessin@gmail.com", "cochiseruhulessin@gmail.com"),
    ("Cochiseruhulessin+foo@gmail.com", "cochiseruhulessin@gmail.com"),
    ("Cochise.ruhulessin+foo@gmail.com", "cochiseruhulessin@gmail.com"),
])
def test_sanitize_email(value: str, result: str):
    assert sanitation.sanitize_email(value) == result