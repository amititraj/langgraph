#from dataclasses import dataclass
from pydantic import BaseModel
from typing import List

#@dataclass
class CustomFile(BaseModel):    
    name:str    
    hash:str
    chunks:List
    
