from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import plans, tasks, quiz, stats
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Personal Learning Platform API",
    description="Yapay zekâ destekli kişisel öğrenme planlama platformu",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans.router)
app.include_router(tasks.router)
app.include_router(quiz.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {
        "message": "AI Personal Learning Platform API is running"
    }