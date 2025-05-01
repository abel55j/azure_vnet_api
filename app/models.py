# Request/Response models

from pydantic import BaseModel
from typing import List

class SubnetModel(BaseModel):
    name: str
    prefix: str

class VNetCreateRequest(BaseModel):
    resource_group: str
    vnet_name: str
    location: str
    address_prefix: str
    subnets: List[SubnetModel]