from tqdm import tqdm

from kukuha.db.api import DBApi
from kukuha.engine import Engine


class KukuhaApp:

    def __init__(self, git_version: str):
        self.engine = Engine(git_version)
        db_version = DBApi.get_git_version(git_version)
        if db_version is None:
            self.git_version_id = DBApi.add_git_version(git_version)
            for query in tqdm(DBApi.get_query_list(), desc='Initialize DB revision:'):
                prompt, row_answer = self.engine.handle_request(query['query'])
                DBApi.update_request_history({
                    'git_version_id': self.git_version_id,
                    'query_id': query['id'],
                    'prompt': prompt,
                    'answer': row_answer
                })
        else:
            self.git_version_id = db_version['id']

    def handle_request(self, query: str) -> str:
        prompt, row_answer = self.engine.handle_request(query)
        DBApi.update_request_history({
            'git_version_id': self.git_version_id,
            'query_id': DBApi.save_query(query),
            'prompt': prompt,
            'answer': row_answer
        })

        return self.engine.filter_answer(row_answer)

    def exit(self) -> None:
        print('Exit Kukuha!')
