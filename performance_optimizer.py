from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import create_engine, Column, String, select
from sqlalchemy.orm import declarative_base, sessionmaker
from cachetools import TTLCache
import time

app = FastAPI()

cache = TTLCache(maxsize=100, ttl=300)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

@app.get("/optimized-data")
async def get_optimized_data(query: str):
    if query in cache:
        return {"cached_data": cache[query]}

    time.sleep(2)
    result = f"Optimized data result for query: {query}"
    cache[query] = result
    return {"data": result}

@app.post("/start-task")
async def start_task(task_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_task, task_id)
    return {"status": "Task started", "task_id": task_id}

def process_task(task_id: str):
    print(f"Processing task {task_id}...")
    time.sleep(5)
    print(f"Task {task_id} completed.")

@app.get("/fetch-users")
async def fetch_users(email: str):
    with SessionLocal() as session:
        query = select(User).where(User.email == email)
        result = session.execute(query).scalars().first()
        return {"user_data": result}

