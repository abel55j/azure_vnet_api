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

# app/database.py
import json
import os

db_path = "vnet_data.json"

def save_data(data):
    with open(db_path, "w") as f:
        json.dump(data, f)

def load_data():
    if not os.path.exists(db_path):
        return []
    with open(db_path, "r") as f:
        return json.load(f)