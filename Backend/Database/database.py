from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv
from Backend.User.user_model import User

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_engine(postgres_url)

def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_database():
    try:
        confirmation = input("WARNING: This will delete all tables in the database. Are you sure? (yes/no): ").strip().lower()
        if confirmation == "yes":
            SQLModel.metadata.drop_all(engine)
            print("All tables have been deleted successfully.")
        else:
            print("Operation canceled. No tables were deleted.")
    except Exception as e:
        print(f"Error while deleting tables: {e}")