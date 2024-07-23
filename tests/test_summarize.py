import pytest
from unittest.mock import AsyncMock
from utils import parse_srt, summarize_text
from dto import SubtitleDTO, SummaryDTO


@pytest.mark.asyncio
async def test_parse_srt():
    srt_file_path = "tests/example.srt"

    subtitles = await parse_srt(srt_file_path, count=2)
    assert len(subtitles) == 2
    assert subtitles[0] == SubtitleDTO(
        start="00:00:00,000",
        end="00:00:02,500",
        text="Welcome to the Example Subtitle File!"
    )
    assert subtitles[1] == SubtitleDTO(
        start="00:00:03,000",
        end="00:00:06,000",
        text="This is a demonstration of SRT subtitles."
    )


@pytest.mark.asyncio
async def test_summarize_text(mocker):
    text = "First subtitle text. Second subtitle text."
    summarize_prompt_path = './prompts/summarize.yaml'
    llm_model = mocker.MagicMock()

    expected_summary = "This is a summary."
    mock_load_chain = mocker.patch('langchain.chains.summarize.load_summarize_chain')
    mock_chain = AsyncMock()
    mock_chain.arun.return_value = expected_summary
    mock_load_chain.return_value = mock_chain

    summary = await summarize_text(text, summarize_prompt_path, llm_model)
    assert summary == SummaryDTO(summary=expected_summary)
    mock_chain.arun.assert_called_once_with(text)
