from fastapi import FastAPI
from database import create_db_and_tables
import uvicorn
import os

app = FastAPI()

create_db_and_tables()

print("1")

@app.get("/")
def root():
    return {"Message": "FuriGen API"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('BACK_DOMAIN'), port=int(os.getenv('BACK_PORT')))
