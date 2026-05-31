from fastapi import FastAPI, Depends, HTTPException
from database import engine,sessionlocal,base 
from schemas import Todo as TodoSchema, Todocreate 
from sqlalchemy.orm import Session 
from model import Todo

base.metadata.create_all(bind=engine) 

app=FastAPI() 

def get_db() : 
    db=sessionlocal() 
    try : 
        yield db 
    finally : 
        db.close() 
        
@app.post("/todos",response_model=TodoSchema) 
def create (todo:Todocreate,db:Session=Depends(get_db)) : 
    db_todo=Todo(**todo.dict()) 
    db.add(db_todo) 
    db.commit() 
    db.refresh(db_todo) 
    return db_todo 

@app.get("/todos",response_model=list[TodoSchema]) 
def read(db:Session=Depends(get_db)) : 
    todo=db.query(Todo).all() 
    return todo 

@app.get("/todos/{todo_id}",response_model=TodoSchema)
def read_id(todo_id:int,db:Session=Depends(get_db)) : 
    todo=db.query(Todo).filter(Todo.id==todo_id).first() 
    if not todo : 
        raise HTTPException(status_code=404,detail='Todo not found') 
    return todo 

@app.put("/todos/{todo_id}",response_model=TodoSchema) 
def update(todo_id:int,updated:Todocreate,db:Session=Depends(get_db)) : 
    todo=db.query(Todo).filter(Todo.id==todo_id).first() 
    if not todo : 
        raise HTTPException(status_code=404,detail='Todo not found') 
    for key,value in updated.dict().items() : 
        setattr(todo,key,value) 
    db.commit() 
    db.refresh(todo) 
    return todo 

@app.delete("/todos/{todo_id}") 
def delete(todo_id:int,db:Session=Depends(get_db)) : 
    todo=db.query(Todo).filter(Todo.id==todo_id).first() 
    if not todo : 
        raise HTTPException(status_code=404,detail='Todo not found') 
    db.delete(todo) 
    db.commit() 
    return {"message":"deleted successfully"} 