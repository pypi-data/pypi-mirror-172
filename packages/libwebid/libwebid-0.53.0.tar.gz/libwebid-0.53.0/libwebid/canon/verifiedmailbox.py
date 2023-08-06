# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pydantic
from libwebid.lib.i18n import gettext as _


class VerifiedMailbox(pydantic.BaseModel):
    """Represents a mailbox that is verified for an account."""
    principal_id: int = pydantic.Field(
        default=...,
        title=_("Principal ID"),
        description=_("Identifies the principal that is used with this mailbox.")
    )

    email: str = pydantic.Field(
        default=...,
        title=_("Email"),
        description=_(
            "The fully-qualified email address of the mailbox."
        )
    )

    verified: datetime.datetime = pydantic.Field(
        default=...,
        title=_("Verified"),
        description=_(
            "The date and time at which the ownership of the mailbox "
            "was last verified."
        )
    )

    def age(self) -> int:
        """Return the age of the last verification, in seconds."""
        return int((self.verified.replace(tzinfo=None) - datetime.datetime.utcnow()).total_seconds())

    def on_domain(self, domain: str) -> bool:
        """Return a boolean indicating if the mailbox is on the given
        domain.
        """
        return str.split(self.email, '@')[-1] == domain