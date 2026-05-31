from pydantic import BaseModel 
from typing import Optional 

class TodoBase(BaseModel) : 
    title:str 
    description:Optional[str] = None 
    completed:bool = False 
    
class Todocreate(TodoBase) : 
    pass 

class Todo(TodoBase) : 
    
    id:int
    class config : 
        orm_mode=True 