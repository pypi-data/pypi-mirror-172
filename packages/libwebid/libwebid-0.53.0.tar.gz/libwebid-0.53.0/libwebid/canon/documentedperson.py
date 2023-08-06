# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import Literal
from libwebid.canon.dateidentityclaim import DateIdentityClaim

import pydantic
from libwebid.lib.i18n import gettext as _

from .genderidentityclaim import GenderIdentityClaim
from .identityclaimtype import IdentityClaimType
from .identitydocumenttype import IdentityDocumentType
from .officialgivennamesclaim import OfficialGivenNameIdentityClaim
from .nameidentityclaim import NameIdentityClaim


class DocumentedPerson(pydantic.BaseModel):
    """Represents a documented person i.e. whose identity is
    assert by a document that was issued by a recognized
    entity.
    """
    given_names: str = pydantic.Field(
        default=...,
        title=_("Given name(s)"),
        description=_(
            "The given name(s) of the person. This property contains one "
            "or more names, depending on the type of document that was used."
        )
    )

    last_name: str = pydantic.Field(
        default=...,
        title=_("Last name"),
        description=_("The last name (family name) of the person.")
    )

    birthdate: datetime.date = pydantic.Field(
        default=...,
        title="Birthdate"
    )

    ncn: str | None = pydantic.Field(
        default=None,
        title=_("National Citizen Number (NCN)"),
        description=_(
            "The government-issued citizen number, such as the "
            "Burgerservicenummer (BSN)."
        )
    )

    gender: str | None = pydantic.Field(
        default=None,
        title=_("Gender"),
        description=_(
            "The gender of the documented person, if it could be parsed "
            "from the identity document, otherwise `null`."
        )
    )

    def claims(
        self,
        document_type: Literal[
            IdentityDocumentType.id_card,
            IdentityDocumentType.passport,
        ],
        country: str,
        source: str,
        asserted: datetime.datetime,
        ial: int,
        exclude: set[str] | None = None
    ) -> list[IdentityClaimType]:
        """Return the claims regarding the person as a list of
        :class:`~libwebid.canon.IdentityClaim` instances."""
        exclude = exclude or set()
        params: dict[str, Any] = {
            'framework': document_type,
            'source': source,
            'asserted': asserted,
            'ial': ial,
            'country': country
        }
        claims: list[IdentityClaimType] = []
        if 'given_name' not in exclude:
            claims.append(
                OfficialGivenNameIdentityClaim(value=self.given_names, **params)
            )
        if 'family_name' not in exclude:
            claims.append(NameIdentityClaim(name='family_name', value=self.last_name, **params))
        if 'birthdate' not in exclude:
            claims.append(DateIdentityClaim(name='birthdate', value=self.birthdate, **params))
        if 'gender' not in exclude and self.gender is not None:
            claims.append(GenderIdentityClaim(value=self.gender, **params))
        return claims