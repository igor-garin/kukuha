import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from kukuha.db.models import Base
from settings import DATABASE_ENGINE, OPERATIONAL_DB_NAME


class _SQLDb(object):
    def __init__(self, db_name: str, data_base_engine: str) -> None:
        self.engine = create_engine(data_base_engine + db_name, echo=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = self.Session()
        Base.metadata.create_all(self.engine)


class _DB(object):

    def __init__(self) -> None:
        self._db = dict()
        self.data_base_engine = DATABASE_ENGINE

    @property
    def _db_impl(self):
        thread_id = threading.get_ident()

        if thread_id not in self._db:
            _db = _SQLDb(OPERATIONAL_DB_NAME, self.data_base_engine)
            return self._db.setdefault(thread_id, _db)
        else:
            return self._db[thread_id]

    @property
    def session(self):
        return self._db_impl.session

    @property
    def metadata(self):
        return self._db_impl.metadata

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise
        else:
            self.session.rollback()


sql_db = _DB()
