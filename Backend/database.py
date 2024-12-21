from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv
from models import Tag, Kana, Kanji, Sense, Entry

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_engine(postgres_url,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def delete_all_databases():
    try:
        SQLModel.metadata.drop_all(engine)
        print("All tables have been deleted successfully.")
    except Exception as e:
        print(f"Error while deleting tables: {e}")
