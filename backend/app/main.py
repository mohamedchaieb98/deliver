import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.init_db import get_database_stats, init_database, seed_sample_data

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A comprehensive water delivery management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    print("\n" + "=" * 60)
    print("🚀 STARTING WATER DELIVERY MANAGEMENT SYSTEM")
    print("=" * 60)

    # Initialize database
    if init_database():
        print("[INFO] Database initialization successful!")

        # Get and display database stats
        stats = get_database_stats()
        if stats:
            print("[INFO] Database Statistics:")
            for table, count in stats.items():
                print(f"  - {table.capitalize()}: {count} records")

        # Add sample data if database is empty
        if stats and all(count == 0 for count in stats.values()):
            print("[INFO] Database is empty, adding sample data...")
            seed_sample_data()

    else:
        print("[ERROR] Database initialization failed!")
        print("[INFO] Please check your database configuration")

    print("\n[INFO] API Server is ready!")
    print(f"[INFO] API Documentation: http://localhost:8000/docs")
    print(f"[INFO] API Base URL: http://localhost:8000/api/v1")
    print("=" * 60 + "\n")


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": "Water Delivery Management System API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/database/status")
async def database_status():
    """Get database status and statistics"""
    try:
        stats = get_database_stats()
        if stats is not None:
            return {
                "status": "connected",
                "tables": stats,
                "total_records": sum(stats.values()),
            }
        else:
            return {"status": "error", "message": "Failed to connect to database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
