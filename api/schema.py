from pydantic import BaseModel

class Package(BaseModel):
    id:int
    name:str
    email:str
    curr_status:str
    prev_status:str

class ShippingProvider(BaseModel):
    id: int
    name: str
    address: str
    phone: str
