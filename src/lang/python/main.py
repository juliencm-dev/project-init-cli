from uvicorn import run
from server import create_app
from server.config import settings as s

development = s.FASTAPI_ENV == "development"

app = create_app()

@app.get("/")
async def root():
    return {"message": "Front end is working"}

if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8001, reload=development)
