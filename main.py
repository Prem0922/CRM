from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import router
from database import Base, engine
from routers import auth
import models

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router)

# Include auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# --- Admin endpoints for DB management ---
@app.post("/admin/generate-data")
def generate_data():
    try:
        from generate_data import main as generate_main
        generate_main()
        return {"status": "success", "message": "Data generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/delete-db")
def delete_db():
    try:
        from delete_db import delete_database
        delete_database()
        return {"status": "success", "message": "Database deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Do NOT run uvicorn here; Render will do it for you 
