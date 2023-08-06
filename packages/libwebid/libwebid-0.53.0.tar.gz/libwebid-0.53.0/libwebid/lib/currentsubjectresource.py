# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from cbra.conf import settings
from cbra.exceptions import Forbidden
from cbra.exceptions import NotFound
from cbra.ext.oauth2 import RFC9068Principal
from cbra.ext.oauth2.params import LocalIssuer
from cbra.params import ServerKeychain
from cbra.resource import Resource
from ckms.core import Keychain
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from .storageencrypter import StorageEncrypter
from .subjectesolver import SubjectResolver
from .subject import Subject
from .resourceprincipal import ResourcePrincipal


security: HTTPBearer = HTTPBearer(auto_error=False)


class CurrentSubjectResource(Resource):
    """Authenticates the Subject using the `subject_id` path parameter."""
    __module__: str = 'libwebid.lib'
    encrypter: StorageEncrypter = StorageEncrypter.inject()
    resolver: SubjectResolver = fastapi.Depends(SubjectResolver)
    principal: ResourcePrincipal # type: ignore
    service_scope: set[str] = {"webidentityapis.com/internal"}
    subject_id: int
    trusted_issuers: set[str] = set()
    if hasattr(settings, 'TRUSTED_ISSUERS'):
        trusted_issuers = settings.TRUSTED_ISSUERS

    @classmethod
    async def principal_factory(
        cls,
        request: fastapi.Request,
        issuer: str = LocalIssuer,
        bearer: HTTPAuthorizationCredentials | None = fastapi.Depends(security),
        keychain: Keychain = ServerKeychain,
    ) -> ResourcePrincipal:
        """Inspect the ``Authorization`` header for a valid JSON Web Token (JWT)
        that is issued by a trusted authorization server, and return corresponding
        principal instance.
        """
        factory = RFC9068Principal(
            principal_factory=lambda x: x, # type: ignore
            trusted_issuers=cls.trusted_issuers
        )
        claims = await factory(request, issuer, bearer, keychain)
        return ResourcePrincipal.parse_obj(claims.dict())

    async def authenticate(self) -> None:
        if self.principal.is_subject():
            self.subject = await self.resolver.resolve(self.principal) # type: ignore

    async def authorize( # type: ignore
        self,
        subject_id: int | str
    ) -> None:
        if isinstance(subject_id, str) and subject_id != 'me':
            raise NotFound
        elif subject_id == 'me' and self.principal.is_service():
            # Services can not access Subject resources using the
            # me parameter, since we cannot determine for which
            # Subject the resource is being accessed.
            raise NotFound
        elif self.principal.is_service()\
        and not self.principal.has_scope(self.service_scope):
            raise Forbidden
        elif self.principal.is_service():
            assert isinstance(subject_id, int) # nosec
            self.subject_id = subject_id
        elif subject_id == 'me' and self.principal.is_subject():
            assert isinstance(self.subject, Subject) # nosec
            self.subject_id = self.subject.sub
        elif isinstance(subject_id, int) and self.principal.is_subject():
            if self.principal.sub != subject_id:
                raise Forbidden
            assert isinstance(self.subject, Subject) # nosec
            self.subject_id = self.subject.sub
        else:
            raise NotImplementedError