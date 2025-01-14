from bson.errors import InvalidId
from fastapi import HTTPException
from starlette.responses import JSONResponse

from models import StudentModel
from database import collection
from bson import ObjectId





async def create_student(student: StudentModel):
    new_student = student.model_dump(exclude=["id"])
    result = await collection.insert_one(new_student)
    new_student['id'] = str(result.inserted_id)
    return new_student


async def show_student(id: str):

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    student = await collection.find_one({"_id": ObjectId(id)})

    if not student:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")

    student["id"] = str(student["_id"])
    del student["_id"]
    return  StudentModel(**student)



async def delete_student(id: str) -> JSONResponse:
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")


    return JSONResponse(content={"message": "Item deleted successfully"})


async def update_student(id: str, student: StudentModel):
    if isinstance(student, dict):
        student = StudentModel(**student)
    updated_item = student.model_dump(exclude=["id"])
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_item}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item["id"] = id
    return StudentModel(**updated_item)




