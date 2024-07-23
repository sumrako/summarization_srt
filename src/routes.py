import os
from typing import List
from langchain_community.chat_models.gigachat import GigaChat
from fastapi import APIRouter, Query
from fastapi import HTTPException
from pydantic import FilePath

from utils import parse_srt, summarize_text
from dto import SubtitleDTO, SummaryDTO
from configs import GIGACHAT_CONFIG


DEFAULT_SRT_PATH = './tests/example.srt'
subtitles_router = APIRouter()


@subtitles_router.get("/subtitles", response_model=List[SubtitleDTO] | None)
async def get_subtitles(
    srt_path: FilePath = Query(DEFAULT_SRT_PATH, description="Путь к .srt файлу"),
    count: int = Query(10, description="Количество сегментов для возврата")
):
    if not os.path.exists(srt_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
        
    return await parse_srt(srt_file_path=srt_path, count=count)


@subtitles_router.get("/summarize", response_model=SummaryDTO)
async def get_summarize(srt_path: FilePath = Query(DEFAULT_SRT_PATH, description="Путь к .srt файлу")):
    if not os.path.exists(srt_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    giga = GigaChat(credentials=GIGACHAT_CONFIG.gigachat_auth_data, verify_ssl_certs=False)
    srts = await parse_srt(srt_file_path=srt_path)
    text = ' '.join([item.text for item in srts])
    summarize_prompt_path = './prompts/summarize.yaml'
    return await summarize_text(text, summarize_prompt_path, giga)
