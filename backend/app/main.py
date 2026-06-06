from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Document Intelligence Agent",
    description="AI-powered document analysis platform",
    version="0.1.0"
)

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