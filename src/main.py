from fastapi import FastAPI
from routes import subtitles_router


app = FastAPI()

app.include_router(subtitles_router)
