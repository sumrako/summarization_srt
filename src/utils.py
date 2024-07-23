import re
import aiofiles
from typing import List
from dto import SubtitleDTO, SummaryDTO
from langchain.base_language import BaseLanguageModel
from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain


async def parse_srt(srt_file_path: str, count: int | None = None) -> List[SubtitleDTO]:
    async with aiofiles.open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_data = await file.read()

        srt_pattern = re.compile(
            r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL
        )

        subtitles = [
            SubtitleDTO(
                start=match.group(2),
                end=match.group(3),
                text=match.group(4).replace('\n', ' ')
            ) for match in srt_pattern.finditer(srt_data)
        ]

        return subtitles if count is None else subtitles[:count]


async def summarize_text(text: str, prompt_file_path: str, llm_model: BaseLanguageModel) -> SummaryDTO:
    map_prompt = load_prompt(prompt_file_path)
    chain = load_summarize_chain(llm_model, chain_type="map_reduce", map_prompt=map_prompt)
    summarized_text = await chain.arun(text)
    return SummaryDTO(summary=summarized_text)
