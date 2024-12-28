from uvicorn import run
from server import create_app, config
from server.router import api

development = True if config.FASTAPI_ENV == "development" else False

app = create_app()

app.include_router(api.router)

@app.get("/")
async def root():
    return {"message": "Front end is working"}

if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=development)
