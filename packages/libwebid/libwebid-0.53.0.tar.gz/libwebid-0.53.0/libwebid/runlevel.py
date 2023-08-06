# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext import ioc
from libwebid.infra.services import EmailService


async def init():
    """Loads the preconfigured dependencies in the default provider."""
    if not ioc.is_satisfied('EmailService'):
        ioc.provide('EmailService', EmailService)