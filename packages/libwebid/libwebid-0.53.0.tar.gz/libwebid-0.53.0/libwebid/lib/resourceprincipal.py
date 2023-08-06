# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from cbra.ext.oauth2.types import IPrincipal

from .serviceprincipal import ServicePrincipal
from .subjectprincipal import SubjectPrincipal


class ResourcePrincipal(pydantic.BaseModel, IPrincipal):
    __root__: (
        ServicePrincipal |
        SubjectPrincipal
    )

    @property # type: ignore
    def sub(self) -> int:
        assert isinstance(self.__root__, SubjectPrincipal), repr(self.__root__) # nosec
        return self.__root__.sub

    def is_authenticated(self) -> bool:
        return True

    def get_current_scope(self) -> set[str]:
        return self.__root__.get_current_scope()

    def has_scope(self, scope: str | set[str]) -> bool:
        return self.__root__.has_scope(scope)

    def is_service(self) -> bool:
        return isinstance(self.__root__, ServicePrincipal)

    def is_subject(self) -> bool:
        return isinstance(self.__root__, SubjectPrincipal)