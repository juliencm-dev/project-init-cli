from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from server.db import create_db
from server.routes import auth, user
from server.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    #NOTE: This is where you can add your own startup logic.
    print("Server is starting on port 8001")
    await create_db() 

    yield

    #NOTE: This is where you can add your own shutdown logic.
    print("Server is shutting down")

def create_app():
    app = FastAPI(
        title="Your App Name",
        description="Project structure for your FastAPI app.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(auth.router)
    app.include_router(user.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
