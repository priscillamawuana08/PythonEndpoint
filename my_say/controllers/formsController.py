from fastapi import APIRouter, Depends, HTTPException, status
from models.formModels import *
from schemas.formsSchema import FormBase
from typing import Annotated
from sqlalchemy.orm import Session
from database.databaseConnection import SessionLocal
import uuid
import logging
import os
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder



#Console Logging
log_level = logging.INFO
if os.environ.get('DEBUG'):
    log_level = logging.DEBUG
    
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S%p')

logger = logging.getLogger(__name__)



# create a connection to the database
async def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        await db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]




router = APIRouter()





# create forms
@router.post("/forms/create_form")
async def create_forms(form_data: FormBase, db: db_dependency):
    
    form_data = Form(
        name=form_data.name,
        elements=form_data.elements,
        created_by=form_data.created_by
     
    )
    
    async with db.begin():
        db.add(form_data)
        await db.commit()
       
        
    return {"message": "User form created successfully", "data": form_data}


# get by id
@router.get("/forms/get_form_by_id/{id}")
async def get_form_by_id(id : uuid.UUID, db:db_dependency):
    
    result = await db.execute(select(Form).where(Form.id == id))
    form_data = result.scalar()
  

    if form_data is None:
        raise HTTPException(status_code=404, detail="Form not found",headers={"message": "id listed in the form", "data": "[]"})
    
    return form_data 


#get all forms
@router.get("/forms/get_all_forms")
async def get_all_forms(db:db_dependency):
    result = await db.execute(select(Form))
    form_data = result.scalars().all()
    
    if form_data is None:
        raise HTTPException(status_code=200, detail="Form is empty or null", headers={"message": "id listed in the form", "data": "[]"})
    
    return form_data

    
# update form(put)
@router.put("/forms/update_all_forms_fields/{id}")
async def update_form(id :uuid.UUID, db:db_dependency, form_input : FormBase):
    form_data = await db.get(Form, id)
    if form_data == None:
        raise HTTPException(status_code=200, detail="Form is empty or null", data = form_data)
    results = form_input.__dict__
    for key, value in results.items():
        setattr(form_data, key, value)
            
    db.add(form_data)
    await db.commit()
  
    return form_data



# update an instance in a form (patch)
@router.patch("/forms/update_individual_form_fields/{id}")
async def update_form(id: uuid.UUID, db: db_dependency, form_input: dict):
    form_data = await db.get(Form, id)
    converted_form_data = form_data.__dict__
    inputs = form_input
    result = {}
    
    for key1, value1 in converted_form_data.items():
        for key2 ,value2 in inputs.items():
            if key1 == key2:
                result[key2] = value2
                
                
            elif key1 != key2 :
                result[key1] =  value1
    
    for key, value in result.items():
        setattr(form_data, key, value)
    

    db.add(form_data)
    await db.commit()
    await db.refresh(form_data)
  
    return form_data

    
# delete form
@router.delete("/forms/delete_forms/{id}")
async def update_form(id :uuid.UUID, db:db_dependency):
    form_data = await db.get(Form, id)
    
    if not form_data:
        raise HTTPException(
            status_code=404, 
            detail="Form not found",
            headers={"message": "id listed in the form", "data": "[]"},
        )
    
    await db.delete(form_data)
    await db.commit()
    
    return "Form delete complete"