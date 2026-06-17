from fastapi import FastAPI

# Import routers
from app.api.upload import router as upload_router


# --------------------------------
# Application Configuration
# --------------------------------
# Creates the FastAPI application
# and defines metadata used by Swagger
# --------------------------------
app = FastAPI(
    title="Enterprise Document Intelligence Agent",
    description="AI-powered document analysis platform",
    version="0.1.0"
)


# --------------------------------
# Register Routers
# --------------------------------
# Makes endpoint groups available
# to the application
# --------------------------------
app.include_router(upload_router)


# --------------------------------
# Health & Status Endpoints
# --------------------------------
# Used for monitoring and testing
# --------------------------------
@app.get("/")
def root():
    return {
        "message": "Enterprise Document Intelligence Agent API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }