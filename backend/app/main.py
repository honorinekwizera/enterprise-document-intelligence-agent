from fastapi import FastAPI

# Import routers
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.stats import router as stats_router

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
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(stats_router)


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