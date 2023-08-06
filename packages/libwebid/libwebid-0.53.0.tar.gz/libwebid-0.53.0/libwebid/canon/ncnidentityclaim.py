# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic
from libwebid.lib.i18n import gettext as _

from .stringidentityclaim import StringIdentityClaim


class NCNIdentityClaim(StringIdentityClaim):
    """A :class:`~libwebid.lib.IdentityClaim` implementation that
    represents a National Citizen Number (NCN).
    """
    kind: Literal['ncn'] = 'ncn' # type: ignore

    name: Literal['ncn'] = pydantic.Field(
        default='ncn',
        title=_("Name"),
        description=_("Is always `ncn`"),
        enum=['ncn',]
    )

    country: str = pydantic.Field(
        default=...,
        title=_("Country"),
        description=_(
            "The country that issued the National Citizen Number (NCN), "
            "represented as a numeric ISO 3166 country code."
        ),
        min_length=3,
        max_length=3
    )