from fastapi import APIRouter 
from models import StudentModel


from services.services_CRUD import create_student , show_student , update_student , delete_student


router = APIRouter()

@router.post("/students/", response_model=StudentModel)
async def create_student_route(student:StudentModel):
    return await create_student(student)

@router.get("/students/{id}",response_model=StudentModel)
async def show_student(id: str):
    return await show_student(id)
   



@router.delete("/students/{id}",response_model=StudentModel)
async def delete_student(id:str):
    return await delete_student(id)
    
   
@router.put("/students/{id}",response_model = StudentModel)
async def update_student(id:str,student:StudentModel):
    update_data = student.model_dump(exclude_unset=True)
    return await update_student(id,update_data)


  
   


