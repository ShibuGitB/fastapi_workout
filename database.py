from sqlalchemy import create_engine 
from dotenv import load_dotenv  
import os 
from sqlalchemy.orm import sessionmaker, declarative_base 

load_dotenv() 
database_url=os.getenv("DATABASE_URL")  
engine=create_engine(database_url) 
sessionlocal=sessionmaker(bind=engine,autoflush=False) 
base=declarative_base() 