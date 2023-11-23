from sqlalchemy import Boolean, Column, Integer, String, UUID, DateTime,func, JSON, ARRAY, text
from database.databaseConnection import Base
import datetime
from typing import List



class Form(Base):
  __tablename__ = 'form'
  
  id = Column(UUID(as_uuid=True), primary_key=True, server_default= text("uuid_generate_v4()"), unique=True, index=True)
  name= Column(String, nullable=False)
  elements = Column(JSON, nullable=False)
  created_on = Column(DateTime, nullable=False, default=func.current_timestamp())
  created_by = Column(String, nullable=False, default="Not indicated")
  updated_on = Column(DateTime, nullable=True, default=func.current_timestamp())
  updated_by = Column(String, nullable=True, default="Not updated")
  
  
  
 