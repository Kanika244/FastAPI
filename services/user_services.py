from database import user_collection
from models import User
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
 
async def register_user(user:User):
     user_in_db=await user_collection.find_one({"email":user.email})
     if user_in_db:
        raise HTTPException(status_code=400,detail="Already registered")
     
     hashed_pass = pwd_context.hash(user.password)

     user_dict=user.model_dump()
     user_dict["password"]=hashed_pass
     await user_collection.insert_one(user_dict)
     return User(**user_dict)

async def login_user(email:str,password:str):
     user_in_db= await user_collection.find_one({"email":email})
     temp =  pwd_context.hash(password)
     if not user_in_db or pwd_context.verify(temp,user_in_db["password"]):
        raise HTTPException(status_code=401,detail="Invalid login or password")
     return {"message":"Login Successful","User":User(**user_in_db)}