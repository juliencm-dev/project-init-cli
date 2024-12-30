from fastapi.middleware.cors import CORSMiddleware
from server.config import settings as s

def register_middlewares(app):
    #NOTE: This is where you can add your own middlewares.
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=s.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


