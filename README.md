# Azure VNet API using FastAPI

## 🚀 Overview

This project provides a FastAPI-based REST API that allows authenticated users to:

- ✅ Create Azure Virtual Networks (VNets) with multiple subnets  
- 📄 Retrieve details of all created VNets  
- 🔐 Authenticate using OAuth2 Password Flow (via Azure Entra ID)

---

## 📌 Prerequisites

- A valid Azure account with permission to manage resources
- [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- `az` CLI (optional but recommended)

---

## 🔐 Azure Setup Instructions

### 1. Register App in Azure Entra ID (Azure Active Directory)

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for **App registrations** → Click **New registration**
3. Set:
   - Name: `azure-vnet-api`
   - Supported account types: default
   - Redirect URI: leave blank
4. Click **Register**

### 2. Create and Copy Credentials

- **AZURE_CLIENT_ID**: From App Overview page  
- **AZURE_TENANT_ID**: Also in App Overview  
- **AZURE_CLIENT_SECRET**:  
  - Go to **Certificates & secrets**
  - Click **New client secret**, name it, choose expiration, click **Add**
  - Copy the value immediately!

- **AZURE_SUBSCRIPTION_ID**:  
  - Go to your Azure **Subscriptions** section  
  - Copy the ID of the target subscription

### 3. Assign Role to the App

- Go to **Resource groups** → `test-rg` → **Access control (IAM)**
- Click **+ Add role assignment**
- Assign `Network Contributor` role to your registered app

---

## 🌐 Register Microsoft.Network Resource Provider

### Option 1: Azure Portal

1. Go to **Subscriptions** → Select your subscription  
2. In the left menu, search for **Resource providers**
3. Find `Microsoft.Network` → Click **Register**

> ⚠️ If not visible, make sure your account has **Owner** or **Contributor** role

### Option 2: Azure CLI

```bash
az provider register --namespace Microsoft.Network
```

---

## ⚙️ Local Setup

### 1. Create and Activate Conda Environment

```bash
conda create -n azure-vnet-api python=3.10
conda activate azure-vnet-api
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure `.env` File

Create a file named `.env` in the **project root**:

```env
AZURE_CLIENT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
AZURE_CLIENT_SECRET="your-super-secret-value"
AZURE_TENANT_ID="yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
AZURE_SUBSCRIPTION_ID="zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
```

---

## 🚀 Run the API

```bash
cd azure_vnet_api/
uvicorn app.main:app --reload
```

Open Swagger UI:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 🔐 Login Credentials (Swagger UI)

| Field     | Value     |
|-----------|-----------|
| Username  | `admin`   |
| Password  | `password` |

---

## 📬 API Endpoints

- `GET /` → Root welcome message
- `POST /login` → Authenticate and get bearer token
- `POST /create-vnet` → Create a new Virtual Network
- `GET /get-vnets` → List all created VNets

---

## 🧪 Example Payload for `/vnets/`

```json
{
  "resource_group": "test-rg",
  "vnet_name": "test-vnet",
  "location": "eastus",
  "address_prefix": "10.0.0.0/16",
  "subnets": [
    { "name": "subnet1", "prefix": "10.0.1.0/24" },
    { "name": "subnet2", "prefix": "10.0.2.0/24" }
  ]
}
```

---

## 📁 Project Structure

```
/azure_vnet_api
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── azure_client.py  # Azure interaction logic
│   ├── auth.py          # Authentication logic
│   ├── models.py        # Request/Response models
│   └── database.py      # Simple in-memory storage
├── requirements.txt
├── .env
└── README.md
```
