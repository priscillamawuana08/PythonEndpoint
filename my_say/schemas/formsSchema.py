from pydantic import BaseModel, constr
from typing import List, Dict, Union, Optional

class FormBase(BaseModel):
  name: str
  elements: List[Dict[str, Union[str, int]]]
  created_by: str
  
 

