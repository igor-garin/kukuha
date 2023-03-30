from typing import Tuple


class Engine:

    def handle_request(self, query: str) -> Tuple[str, str]:
        return ('prompt', 'row_answer')

    def filter_answer(self, row_answer: str) -> str:
        return row_answer
