import os
from dotenv import load_dotenv
from database.databaseConnection import engine, SessionLocal, Base

# internal imports
from schemas.formsSchema import *
from models.formModels import *
from controllers.formsController import *

from fastapi import FastAPI, status, Response, Depends
from fastapi.middleware.cors import CORSMiddleware





load_dotenv()



app = FastAPI(
    title= "MySay Form Service",
    version="0.0.1",
    description="FastAPI Forms creation",
    openapi_tags=[
        {
            "name": "Home",
            "description": "Check health of the API"
        }
    ]
)


origins = ['http://localhost:8000','http://127.0.0.1:8000 ']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes 
app.include_router(router, prefix="", tags=["Forms"])



