# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeAlias

from .birthplaceidentityclaim import BirthplaceIdentityClaim
from .dateidentityclaim import DateIdentityClaim
from .genderidentityclaim import GenderIdentityClaim
from .stringidentityclaim import StringIdentityClaim
from .officialgivennamesclaim import OfficialGivenNameIdentityClaim
from .multinameidentityclaim import MultiNameIdentityClaim
from .nameidentityclaim import NameIdentityClaim
from .ncnidentityclaim import NCNIdentityClaim


IdentityClaimType: TypeAlias = (
    GenderIdentityClaim | BirthplaceIdentityClaim | NCNIdentityClaim |
    OfficialGivenNameIdentityClaim | MultiNameIdentityClaim | NameIdentityClaim |
    DateIdentityClaim | StringIdentityClaim
)