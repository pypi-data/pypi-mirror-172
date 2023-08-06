from typing import List, Optional
from pydantic import Field
from fakts.discovery.base import Discovery
from fakts.discovery.static import StaticDiscovery
from fakts.grants.base import FaktsGrant
import ssl
import certifi


class RemoteGrant(FaktsGrant):
    ssl_context: ssl.SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where())
    )
    timeout: int = Field(None, description="Timeout for the remote grant")
    discovery: Discovery = Field(default_factory=StaticDiscovery)
    scopes: List[str] = Field(default_factory=list)
    name: Optional[str] = None

    async def aload(self):
        raise NotImplementedError()

    class Config:
        arbitrary_types_allowed = True
