from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
from dotenv import load_dotenv

from app.api import auth, meals, footprint, swaps, dashboard, challenges, energy, gamification
from app.core.database import engine, SessionLocal
from app.models import Base

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Greenflow Life API",
    description="푸드 카본 레저 앱 API",
    version="1.0.0"
)

# CORS middleware with environment variable support
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
cors_origins = [origin.strip() for origin in cors_origins]  # Remove whitespace

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(meals.router, prefix="/api/meals", tags=["meals"])
app.include_router(footprint.router, prefix="/api/footprint", tags=["footprint"])
app.include_router(swaps.router, prefix="/api/swaps", tags=["swaps"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(challenges.router, prefix="/api/challenges", tags=["challenges"])
app.include_router(energy.router, prefix="/api", tags=["energy"])
app.include_router(gamification.router, prefix="/api/gamification", tags=["gamification"])

@app.get("/")
async def root():
    return {
        "message": "Greenflow Life API", 
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 