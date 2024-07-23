import uvicorn
from fastapi import FastAPI

from routes import subtitles_router
from configs import APP_CONFIG

app = FastAPI()
app.include_router(subtitles_router)


if __name__ == "__main__":
    uvicorn.run(app, **APP_CONFIG.get_uvicorn_attr)
