from fastapi import FastAPI
from database import create_db_and_tables, delete_all_databases
import uvicorn
import os

app = FastAPI()

delete_all_databases()
create_db_and_tables()

@app.get("/")
def root():
    return {"Message": "FuriGen API"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('BACK_DOMAIN'), port=int(os.getenv('BACK_PORT')))
