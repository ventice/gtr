import re
import typing

from openai import AsyncOpenAI

import config

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

_RESPONSE_PATTERN = re.compile(r"(<(..)>(.*)</\2>)", re.M | re.U | re.M)

async def translate(text: str) -> typing.Optional[dict[str, str]]:
    response = await client.responses.create(
        prompt={
            "id": config.PROMPT_ID,
            "version": config.PROMPT_VERSION
        },
        input=text
    )
    if response.output_text.strip() == config.NO_TRANSLATION:
        return None

    return {
        lang: trans
        for _, lang, trans in _RESPONSE_PATTERN.findall(response.output_text)
    }
