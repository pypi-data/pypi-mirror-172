# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.conf import settings
from cbra.cors import DefaultPolicy


CORSPolicy: type[DefaultPolicy] = DefaultPolicy.new(
    allow_credentials=True,
    allowed_origins=getattr(settings, 'CORS_ALLOWED_HOSTS', []),
    allowed_headers={"Content-Type", "Cookies"},
    allowed_response_headers={"Set-Cookie"}
)