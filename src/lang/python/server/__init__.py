from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.config import settings as s
from server.db import create_db
from server.routes import auth, user
from server.middlewares import register_middlewares
from server.exceptions import register_exceptions

API_PREFIX = f"/api/{s.VERSION}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db() 
    #NOTE: This is where you can add your own startup logic.👇
   
    yield
    #NOTE: This is where you can add your own teardown logic.👇
   

def create_app():
    app = FastAPI(
        title="Your App Name",
        description="Project structure for your FastAPI app.",
        version=s.VERSION,
        lifespan=lifespan,
    )

    register_exceptions(app) 
    register_middlewares(app)

    app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["auth"])
    app.include_router(user.router, prefix=f"{API_PREFIX}/users", tags=["users"])

    return app
