from fastapi import  HTTPException
from models import StudentModel
from database import collection
from bson import ObjectId



async def create_student(student:StudentModel):
    new_student = student.model_dump(exclude=["id"])
    result = await collection.insert_one(new_student)
    new_student['id']=str(result.inserted_id)
    return StudentModel(**new_student)


async def show_student(id: str):
        student = await collection.find_one({"_id": ObjectId(id)})
        
        if not student:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

        student["id"] = str(student["_id"])
        del student["_id"]
        return StudentModel(**student)
   

    
async def delete_student(id:str):
    
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Item not found")
    return {"message":"Item deleted successfully"}



async def update_student(id:str,student:StudentModel):
    updated_item = student.model_dump(exclude=["id"])
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_item}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item["id"] = id
    return StudentModel(**updated_item)




