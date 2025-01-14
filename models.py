from pydantic import BaseModel,EmailStr


class StudentModel(BaseModel):
    name: str
    sid:int

class User(BaseModel):
    name:str
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequest(BaseModel):
    username: str
    password: str
