from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting on port 8000")
    yield
    print("Server is shutting down")

def create_app():
    app = FastAPI(
        title="FastAPI",
        description="A simple FastAPI app to demonstrate deploying a Python app.",
        version="0.1.0",
        lifespan=lifespan,
    )

    return app
