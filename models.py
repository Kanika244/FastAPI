from pydantic import BaseModel
from typing import Optional



class StudentModel(BaseModel):
    id:Optional[str]=None
    studentname: str
    sid:int

class User(BaseModel):
    name:str
    email:str
    password:str
