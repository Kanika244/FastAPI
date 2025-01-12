
from fastapi import APIRouter 
from models import User
from services.user_services import register_user,login_user
router = APIRouter()




@router.post("/register",response_model=User)    
async def register(user:User):
   return await register_user(user)

@router.post("/login")
async def login(email:str,password:str):
   return await login_user(email,password)






