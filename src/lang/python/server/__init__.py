from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.db import create_db
from server.routes import auth, user
from server.middlewares import register_middlewares
from server.exceptions import register_exceptions

@asynccontextmanager
async def lifespan(app: FastAPI):
    #NOTE: This is where you can add your own startup logic.
    await create_db() 

    yield

    #NOTE: This is where you can add your own shutdown logic.

def create_app():
    app = FastAPI(
        title="Your App Name",
        description="Project structure for your FastAPI app.",
        version="0.1.0",
        lifespan=lifespan,
    )

    register_exceptions(app) 
    register_middlewares(app)

    app.include_router(auth.router)
    app.include_router(user.router)

    return app
