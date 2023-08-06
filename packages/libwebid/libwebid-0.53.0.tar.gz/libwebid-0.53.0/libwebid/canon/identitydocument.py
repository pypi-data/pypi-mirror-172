# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import hashlib

import pydantic

import iso3166
from libwebid.lib.i18n import gettext as _

from .documentedperson import DocumentedPerson
from .identityclaimtype import IdentityClaimType
from .identitydocumenttype import IdentityDocumentType


class IdentityDocument(pydantic.BaseModel):
    """Represents a document that identifies a person, such as a
    passport or national identity card.
    """
    document_type: IdentityDocumentType = pydantic.Field(
        default=...,
        title=_("Document type"),
        description=_("Indicates the type of document.")
    )

    document_number: str = pydantic.Field(
        default=...,
        title=_("Document number"),
        description=_("The document number as assigned by the issuer.")
    )

    issue_number: str = pydantic.Field(
        default='',
        title=_("Issue number"),
        description=_("The issue number as assigned by the issuer.")
    )

    country: str = pydantic.Field(
        default=...,
        title=_("Issueing country"),
        description=_(
            "An ISO 3166 numeric country code identifying the country "
            "that issued the official document. If the document was "
            "issued by a non-state actor that is a recognized authority,"
            "`country` has the value of `999`."
        )
    )

    valid_from: datetime.date = pydantic.Field(
        default=...,
        title=_("Valid from"),
        description=_(
            "The date from which the document is valid."
        )
    )

    valid_until: datetime.date = pydantic.Field(
        default=...,
        title=_("Valid until"),
        description=_(
            "The date until which the document is valid."
        )
    )

    person: DocumentedPerson = pydantic.Field(
        default=...,
        title=_("Documented person"),
        description=_(
            "The person that is documented by this identity document."
        )
    )

    @pydantic.validator('country', pre=True)
    def preprocess_country(
        cls,
        value: str | None
    ) -> str | None:
        if isinstance(value, str) and len(value) in (2, 3):
            try:
                country = iso3166.countries.get(value) # type: ignore
            except KeyError:
                raise ValueError(f'Invalid ISO-3166 code: {value}')
            value = country.numeric
        elif isinstance(value, str):
            raise ValueError(f'Not an ISO-3166 code: {value}')
        return value

    def identifier(self) -> str:
        """Return the document identifier that is used to globally identify
        this document. The document is a SHA-256 hash of the document
        properties in the following order:

        1. :attr:`document_type` as an UTF-8 byte-sequence
        2. :attr:`document_number` as an UTF-8 byte-sequence.
        3. :attr:`issue_number` as an UTF-8 byte-sequence. If
           the issuer does not use numbered documents, this is an
           empty string.
        4. :attr:`country` as an UTF-8 byte-sequence.
        5. :attr:`valid_from` represented as the ordinal date on the
           Gregorian calendar, as an unsigned 4-byte integer in the
           Big Endian byteorder.
        6. :attr:`valid_until` represented as the ordinal date on the
           Gregorian calendar, as an unsigned 4-byte integer in the
           Big Endian byteorder.
        """
        h = hashlib.sha3_256()
        h.update(str.encode(self.document_type.value, 'utf-8'))
        h.update(str.encode(self.document_number.upper(), 'utf-8'))
        h.update(str.encode(self.issue_number.upper(), 'utf-8'))
        h.update(str.encode(self.country.upper(), 'utf-8'))
        h.update(int.to_bytes(self.valid_from.toordinal(), 4, 'big', signed=False))
        h.update(int.to_bytes(self.valid_until.toordinal(), 4, 'big', signed=False))
        return h.hexdigest()

    def aggregate(
        self,
        source: str,
        ial: int,
        asserted: datetime.datetime | None = None
    ) -> list[IdentityClaimType]:
        """Return a :class:`~libwebid.canon.IdentityClaimAggregate` instance
        containing the claims asserted by this document.
        """
        asserted = asserted or datetime.datetime.utcnow().replace(
            second=0,
            microsecond=0
        )
        assert self.document_type in (
            IdentityDocumentType.id_card,
            IdentityDocumentType.passport
        ) # nosec
        return [
            *self.person.claims(
                source=source,
                document_type=self.document_type,
                country=self.country,
                ial=ial,
                asserted=asserted
            )
        ]

    def is_valid(self) -> bool:
        """Return a boolean indicating if the document is valid,
        based on :attr:`valid_until`.
        """
        return self.valid_until < datetime.date.today()