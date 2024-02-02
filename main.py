from fastapi import FastAPI, HTTPException, Depends, Header
from httpx import AsyncClient
import httpx
from pydantic import BaseModel,EmailStr
import requests

app = FastAPI()

class add_beneficiary(BaseModel):
    beneId: int
    name: str
    email: EmailStr
    phone: str
    bankAccount: str
    ifsc: str
    vpa: str
    address1: str
    address2: str
    city: str
    state: str
    pincode: int

async def get_authorization_header(x_client_id: str = Header(...), x_client_secret: str = Header(...)):
    return {
        "accept": "application/json",
        "x-client-id": x_client_id,
        "x-client-secret": x_client_secret
    }

async def authorize(headers: dict = Depends(get_authorization_header)):
    url = "https://payout-gamma.cashfree.com/payout/v1/authorize"

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers)

    return response.json()

async def get_add_beneficiary_headers(authorization: str = Header(...)):
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": authorization
    }

@app.get("/authorize")
async def authorize_endpoint(result: str = Depends(authorize)):
    return {"authorization_result": result}

@app.post("/add_beneficiary")
async def add_beneficiary(token: str,beneId: str, name: str, email: str, phone: str, bankAccount: str, ifsc: str, address1: str, city: str, state: str, pincode: str):
    url = "https://payout-gamma.cashfree.com/payout/v1/addBeneficiary"

    payload = {
        "beneId": beneId,
        "name": name,
        "email": email,
        "phone": phone,
        "bankAccount": bankAccount,
        "ifsc": ifsc,
        "address1": address1,
        "city": city,
        "state": state,
        "pincode": pincode
    }
    
    headers = {
        "accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return {"message": "Beneficiary added successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/get_beneficiary/{bene_id}")
async def get_beneficiary(bene_id: int, token: str):
    url = f"https://payout-gamma.cashfree.com/payout/v1/getBeneficiary/{bene_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/get_bene_id")
async def get_bene_id(bank_account: str, ifsc: str, token: str):
    url = f"https://payout-gamma.cashfree.com/payout/v1/getBeneId?bankAccount={bank_account}&ifsc={ifsc}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.post("/remove_beneficiary")
async def remove_beneficiary(bene_id: str, token: str):
    url = "https://payout-gamma.cashfree.com/payout/v1/removeBeneficiary"

    payload = {
        "beneId": bene_id
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return {"message": "Beneficiary removed successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@app.get("/bene_history/{bene_id}")
async def bene_history(bene_id: int, token: str):
    url = f"https://payout-gamma.cashfree.com/payout/v1/beneHistory?beneId={bene_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)