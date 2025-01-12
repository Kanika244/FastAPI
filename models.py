from pydantic import BaseModel,EmailStr


class StudentModel(BaseModel):
    name: str
    sid:int

class User(BaseModel):
    name:str
    email:EmailStr
    password:str