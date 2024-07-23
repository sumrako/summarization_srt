from typing import List
from langchain.chat_models.gigachat import GigaChat
from fastapi import APIRouter, Query
from pydantic import FilePath
from utils import parse_srt, summarize_text
from dto import SubtitleDTO, SummaryDTO
from configs import GIGACHAT_CONFIG


subtitles_router = APIRouter()


@subtitles_router.get("/subtitles", response_model=List[SubtitleDTO] | None)
async def get_subtitles(
    srt_path: FilePath = Query(description="Путь к .srt файлу"),
    count: int = Query(10, description="Количество сегментов для возврата")
):
    return await parse_srt(srt_file_path=srt_path, count=count)


@subtitles_router.get("/summarize", response_model=SummaryDTO)
async def get_summarize(
    srt_path: FilePath = Query(description="Путь к .srt файлу")
):
    giga = GigaChat(credentials=GIGACHAT_CONFIG.gigachat_client_secret)
    srts = await parse_srt(srt_file_path=srt_path)
    text = ' '.join([item.text for item in srts])
    summarize_prompt_path = './prompts/summarize.yaml'
    return await summarize_text(text, summarize_prompt_path, giga)
