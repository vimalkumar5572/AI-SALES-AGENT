from pydantic import BaseModel
class LeadCreate(BaseModel):
    name:str
    phone:str