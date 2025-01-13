import jwt
from database import user_collection
from models import User
from fastapi import HTTPException
from passlib.context import CryptContext
import datetime

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
secret_key= "hello123"
algorithm = "HS256"
access_token_expire=30
 
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
     
     access_token = create_access_token(data={"email":user_in_db["email"]})
     return {"message":"Login Successful","access_token":access_token}

def create_access_token(data:dict):
    to_encode  = data.copy()
    
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = access_token_expire)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return encode_jwt
