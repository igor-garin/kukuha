from typing import Tuple, List

import openai

import settings

openai.api_key = settings.OPENAI_API_KEY


def gpt_query(prompt: str) -> Tuple[str, int]:
    res = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['message']['content'].strip(), res['usage']['total_tokens']


def openai_embeds(input_text: List[str]) -> Tuple[List[List[float]], int]:
    assert len(input_text) > 0
    res = openai.Embedding.create(input=input_text, engine=settings.OPENAI_EMBED_MODEL)
    embeds = [d['embedding'] for d in res['data']]
    return embeds, res['usage']['total_tokens']


def openai_single_embed(input_text: str) -> Tuple[List[float], int]:
    emds, usage = openai_embeds([input_text])
    return emds[0], usage
