import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from dto import SubtitleDTO
from main import app


@pytest.mark.asyncio
async def test_get_subtitles():
    srt_file_path = "tests/example.srt"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/subtitles", params={"srt_path": srt_file_path, "count": 2})
        assert response.status_code == 200
        subtitles = response.json()
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
async def test_get_summarize(mocker):
    srt_file_path = "tests/example.srt"

    expected_summary = "This is a summary."
    mock_load_chain = mocker.patch('langchain.chains.summarize.load_summarize_chain')
    mock_chain = AsyncMock()
    mock_chain.arun.return_value = expected_summary
    mock_load_chain.return_value = mock_chain

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/summarize", params={"srt_path": srt_file_path})
        assert response.status_code == 200
        summary = response.json()
        assert summary == {"summary": expected_summary}
