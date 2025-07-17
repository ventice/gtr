import re

from openai import AsyncOpenAI

import config

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

_RESPONSE_PATTERN = re.compile(r"(<(..)>(.*)</\2>)", re.M | re.U | re.M)

async def translate(text: str) -> dict[str, str]:
    response = await client.responses.create(
        prompt={
            "id": config.PROMPT_ID,
            "version": config.PROMPT_VERSION
        },
        input=text
    )
    return {
        lang: trans
        for _, lang, trans in _RESPONSE_PATTERN.findall(response.output_text)
    }
