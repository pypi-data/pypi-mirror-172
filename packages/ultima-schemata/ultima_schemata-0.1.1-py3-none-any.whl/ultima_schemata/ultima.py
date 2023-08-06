import logging
# import httpx
from cvss import CVSS3
from datetime import datetime
from pydantic import UUID4, BaseModel, IPvAnyAddress, IPvAnyNetwork, validator 
from typing import Optional
from enum import Enum
from os import environ 
from uuid import uuid4

# client = httpx.Client(
#     base_url=environ.get("CVE_SEARCH_API", "https://cve.circ.lu/api"),
#     timeout=float(environ.get("CVE_SEARCH_TIMEOUT", 10.0)),
#     transport=httpx.HTTPTransport(retries=environ.get("CVE_SEARCH_RETRIES", 3)),
#     headers={
#         "user-agent": environ.get("CVE_SEARCH_USER_AGENT", "ultima/0.1.0")
#     }
#     )

logger = logging.getLogger('schemas')

class Scope(BaseModel):
    ip_blocks: list[IPvAnyNetwork]
    names: list[str]


class Timeline(BaseModel):
    start: datetime
    end: datetime


class Campaign(BaseModel):
    name: str 
    timeline: Timeline 
    scopes: list[Scope] = []
    identifier: UUID4 = uuid4()


# class ResourceType(Enum):
#     server = "server"
#     container = "container"


# class ContainerImage(BaseModel):
#     location: str
#     base: Optional[str]
#     tag: Optional[str]
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
    
#     @validator('location')
#     def docker_hub(cls, v):
#         if v.count('/') == 0:
#             return f"docker.io/library/{v}"
#         elif v.count('/') == 1:
#             return f"docker.io/{v}"
#         else:
#             return v

class NetworkProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    SCTP = "SCTP"

class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    CONNECT = "CONNECT"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    LOCK = "LOCK"
    MKCOL = "MKCOL"
    MOVE = "MOVE"
    PROPFIND = "PROPFIND"
    PROPPATCH = "PROPPATCH"
    UNLOCK = "UNLOCK"
    NONE = "NONE"


class Author(BaseModel):
    name: str 
    

class Asset(BaseModel):
    path: str
    method: HttpMethod = HttpMethod.GET
    url_parameters: list[dict] = []
    body_parameters: list[dict] = []
    discover_date: datetime = datetime.now()
    labels: list[str] = []
    notes: list[dict] = []
      

class Service(BaseModel):
    identifier: UUID4 
    hostname: str = None
    ip: IPvAnyAddress = None
    discover_date: datetime = datetime.now() 
    last_seen: datetime = datetime.now() 
    port: int = 0
    protocol: NetworkProtocol = NetworkProtocol.ICMP
    labels: list[str] = []
    notes: list[dict] = []
    assets: Optional[list[Asset]]
    
    @validator('port')
    def port_checks(cls, v, values):
        if values['protocol'] != NetworkProtocol.ICMP:
            logger.warn(f"Port 0 active for protocol {values['protocol'].value}")
        return v % 65536


class User(BaseModel):
    username: str
    campaign: UUID4
    name: Optional[str] 
    email: Optional[str] 
    password: Optional[str]


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"
    
    
class CWE(BaseModel):
    pass


class CVE(BaseModel):
    identifier: str 
    year: int = 2000 
    summary: str = ""
    # cvss: CVSS3 = None
    cwe: CWE = None 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = int(self.identifier.split('-')[1])
        
    @validator('identifier')
    def check_type(cls, v):
        assert v.startswith("CVE-"), f"{v} does not start with CVE-"
        assert v.count('-') == 2
        assert int(v.split('-')[1]) > 1970, f"Invalid year"
        return v
    


class Finding(BaseModel):
    title: str 
    identifier: UUID4
    resource_id: UUID4
    discover_date: datetime = datetime.now() 
    severity: Severity = Severity.INFO 
    cvss: CVSS3 = None
    score: float = 0.0
    description: str = ""
    cve: CVE = None
    
    class Config:
        arbitrary_types_allowed = True    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.score == 0.0:
            self.severity = Severity.INFO 
        elif self.score < 4.0:
            self.severity = Severity.LOW 
        elif self.score < 7.0:
            self.severity = Severity.MEDIUM
        elif self.score < 9.0:
            self.severity = Severity.HIGH 
        else: 
            self.severity = Severity.CRITICAL
    
    @validator('cvss')
    def check_range(cls, v):
        assert 0 <= v <= 10.0, f"Value not between 0 and 10"
        return v
