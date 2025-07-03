from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .auth.routes import router as auth_router
import os

# Create FastAPI app
app = FastAPI(
    title="Authentication API",
    description="A FastAPI application with Firebase authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Authentication API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Authentication API",
        "docs": "/docs",
        "redoc": "/redoc"
    } 