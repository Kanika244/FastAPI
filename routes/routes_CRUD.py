from fastapi import APIRouter, Depends, HTTPException
from models import StudentModel, User , Token , TokenRequest
from services.services_auth import authenticate_user, create_access_token, get_current_user, fake_users_db

from services.services_CRUD import create_student, show_student, update_student, delete_student

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: TokenRequest):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/students/", response_model=StudentModel)
async def create_student_route(student: StudentModel,current_user: User = Depends(get_current_user)):
    return await create_student(student,current_user)


@router.get("/students/{id}", response_model=StudentModel)
async def show_student_route(id: str):
    return await show_student(id)


@router.delete("/students/{id}", response_model=StudentModel)
async def delete_student_route(id: str):
    return await delete_student(id)


@router.put("/students/{id}", response_model=StudentModel)
async def update_student_route(id: str, student: StudentModel):
    return await update_student(id, student)






