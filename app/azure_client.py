# Azure interaction logic

import os
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetwork, AddressSpace, Subnet
from app.models import VNetCreateRequest
from app.database import load_data, save_data

credential = ClientSecretCredential(
    client_id=os.environ['AZURE_CLIENT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant_id=os.environ['AZURE_TENANT_ID']
)

subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
network_client = NetworkManagementClient(credential, subscription_id)

async def create_vnet_on_azure(request: VNetCreateRequest):
    vnet_params = VirtualNetwork(
        location=request.location,
        address_space=AddressSpace(
            address_prefixes=[request.address_prefix]
        ),
        subnets=[]
    )

    vnet_poller = network_client.virtual_networks.begin_create_or_update(
        request.resource_group,
        request.vnet_name,
        vnet_params
    )
    vnet_result = vnet_poller.result()

    created_subnets = []
    for subnet in request.subnets:
        subnet_params = Subnet(address_prefix=subnet.prefix)
        subnet_poller = network_client.subnets.begin_create_or_update(
            request.resource_group,
            request.vnet_name,
            subnet.name,
            subnet_params
        )
        result = subnet_poller.result()
        created_subnets.append({"name": subnet.name, "prefix": subnet.prefix})

    entry = {
        "resource_group": request.resource_group,
        "vnet_name": request.vnet_name,
        "location": request.location,
        "address_prefix": request.address_prefix,
        "subnets": created_subnets
    }
    data = load_data()
    data.append(entry)
    save_data(data)
    return entry