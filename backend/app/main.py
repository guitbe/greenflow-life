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

# CORS middleware with comprehensive Vercel support
cors_origins_env = os.getenv("CORS_ORIGINS", "")

def is_vercel_domain(origin):
    """Check if origin is a Vercel domain"""
    vercel_patterns = [
        ".vercel.app",
        "-vercel.app", 
        ".vercel.com"
    ]
    return any(pattern in origin for pattern in vercel_patterns)

def cors_origin_validator(origin: str):
    """Dynamic CORS origin validation"""
    allowed_origins = []
    
    if cors_origins_env:
        allowed_origins = [origin.strip() for origin in cors_origins_env.split(",")]
    else:
        # Default allowed origins
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "https://my-greenflow-app.vercel.app",
            "https://greenflow-life.vercel.app",
        ]
    
    # Always allow Vercel domains for this project
    if is_vercel_domain(origin) and ("greenflow" in origin or "my-greenflow" in origin):
        return True
        
    return origin in allowed_origins

print(f"CORS Environment: {cors_origins_env or 'Using defaults with Vercel support'}")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:\d+|https://greenflow-life\.vercel\.app|https://my-greenflow.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
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