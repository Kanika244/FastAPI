from fastapi import APIRouter, HTTPException, Depends
from database import user_collection
from models import User
from bson import ObjectId
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "1567fj62kk2jrj7j"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/register", response_model=User)    
async def register(user: User):
    user_in_db = await user_collection.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Already registered")

    hashed_password = hash_password(user.password)
    user_dict = user.dict(exclude={"id"})
    user_dict["id"] = str(ObjectId())
    user_dict["password"] = hashed_password

    await user_collection.insert_one(user_dict)
    return User(**user_dict)


@router.post("/login")
async def login(email: str, password: str):
    user_in_db = await user_collection.find_one({"email": email})
    if not user_in_db or not verify_password(password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid login or password")

    user_data = {"email": user_in_db["email"], "id": str(user_in_db["_id"])}
    access_token = create_access_token(data=user_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return {"user_id": payload["id"], "email": payload["email"]}






