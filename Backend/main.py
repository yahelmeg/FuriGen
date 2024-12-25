from fastapi import FastAPI
from Backend.Kanji.kanji import router as kanji_router
from Backend.Kana.kana import router as kana_router
import uvicorn
import os
import dotenv

app = FastAPI()
dotenv.load_dotenv()

for router in [kana_router, kanji_router]:
    app.include_router(router)

@app.get("/")
def root():
    return {"Message": "FuriGen API"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('BACK_DOMAIN'), port=int(os.getenv('BACK_PORT')))
