from fastapi import APIRouter , Depends
from models import StudentModel


from services.services_CRUD import create_student , show_student , update_student , delete_student
from routes.user_routes import get_current_user

router = APIRouter()

@router.post("/students/", response_model=StudentModel)
async def create_student_route(student:StudentModel,current_user:dict=Depends(get_current_user)):
    return await create_student(student)

@router.get("/students/{id}",response_model=StudentModel)
async def show_student_route(id: str,current_user:dict=Depends(get_current_user)):
    return await show_student(id)
   



@router.delete("/students/{id}",response_model=StudentModel)
async def delete_student_route(id:str,current_user:dict=Depends(get_current_user)):
    return await delete_student(id)
    
   
@router.put("/students/{id}",response_model = StudentModel)
async def update_student_route(id:str,student:StudentModel,current_user:dict=Depends(get_current_user)):
    update_data = student.model_dump(exclude_unset=True)
    return await update_student(id,update_data)


  
   


