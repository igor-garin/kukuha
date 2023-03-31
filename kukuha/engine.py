import logging
from typing import Tuple

import settings
from kukuha.openai_utils import openai_single_embed, gpt_query
from kukuha.pinecone_utils import pinecone_query_embed, pinecone_get_or_create_index, pinecone_upsert_single_embed
from kukuha.promt_utils import get_promt, SUMMARY_PROMT

logger = logging.getLogger(__name__)


class Engine:

    def __init__(self, git_version: str):
        self.index = pinecone_get_or_create_index(
            settings.PINECONE_INDEX_NAME.format(git_version)
        )

    def handle_request(self, query: str) -> Tuple[str, str]:
        prompt = get_promt(query, self.get_context(query))
        row_answer, _ = gpt_query(prompt)
        logger.debug("Answer: " + row_answer)
        self.save_context(query)
        return prompt, row_answer

    def save_context(self, query: str):
        prompt = SUMMARY_PROMT.format('Igor', query)
        context, _ = gpt_query(prompt)
        context += ' Date: 2023-03-30.'
        embed, _ = openai_single_embed(context)
        pinecone_upsert_single_embed(self.index, embed, {'text': context})
        logger.debug('Saved context:' + context)

    def get_context(self, query: str) -> str:
        embed, _ = openai_single_embed(query)
        context = pinecone_query_embed(self.index, embed)
        context = [c['text'] for c in context]
        return '\n'.join(context)

    def filter_answer(self, row_answer: str) -> str:
        return row_answer
