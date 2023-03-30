import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func, ClauseElement

from kukuha.db.db import sql_db
from kukuha.db.models import Query, GitVersion, RequestHistory


def get_or_create(db, model, defaults=None, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance is not None:
        return instance
    else:
        with db as session:
            params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
            params.update(defaults or {})
            instance = model(**params)
            session.add(instance)
            return instance


class DBApi:
    def __init__(self):
        raise Exception("DBApi is a class with static methods only")

    @staticmethod
    def db() -> None:
        return sql_db

    @staticmethod
    def max_query_id() -> int:
        return DBApi.db().session.query(func.max(Query.id)).scalar()

    @staticmethod
    def get_query_list() -> List[Dict[str, Any]]:
        query = DBApi.db().session.query(Query).order_by(Query.timestamp.asc())
        return [q.to_dict() for q in query]

    @staticmethod
    def save_query(query) -> int:
        s = get_or_create(DBApi.db(),
                          Query,
                          query=query,
                          timestamp=datetime.datetime.utcnow())
        return s.id

    @staticmethod
    def get_git_version(version) -> Optional[Dict]:
        instance = (DBApi.db().session.query(GitVersion)
                    .filter(GitVersion.version == version).first())
        if instance:
            return instance.to_dict()
        else:
            return None

    @staticmethod
    def add_git_version(version) -> int:
        s = get_or_create(DBApi.db(), GitVersion, version=version)
        return s.id

    @staticmethod
    def update_request_history(content) -> int:
        s = get_or_create(DBApi.db(),
                          RequestHistory,
                          id=content.get('id', None),
                          git_version_id=content['git_version_id'],
                          query_id=content['query_id'])
        with DBApi.db() as session:
            session.query(RequestHistory).filter(
                RequestHistory.id == s.id
            ).update({
                RequestHistory.git_version_id: content['git_version_id'],
                RequestHistory.query_id: content['query_id'],
                RequestHistory.promt: content['promt'],
                RequestHistory.answer: content['answer'],
            })

        return s.id
