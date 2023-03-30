import datetime

from sqlalchemy import Column, String
from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)


class Query(Base):
    __tablename__ = 'query'

    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(4048))
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'query': self.query, 'timestamp': self.timestamp}


class GitVersion(Base):
    __tablename__ = 'git_version'

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(8))
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'version': self.version, 'timestamp': self.timestamp}


class RequestHistory(Base):
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)
    git_version_id = Column(Integer, ForeignKey(GitVersion.id), nullable=False)
    git_version = relationship("GitVersion")
    query_id = Column(Integer, ForeignKey(Query.id), nullable=False)
    query = relationship("Query")
    prompt = Column(String)
    answer = Column(String)

    def to_dict(self):
        return {'id': self.id, 'timestamp': self.timestamp,
                'git_version_id': self.git_version_id, 'git_version': self.git_version,
                'query_id': self.git_version_id, 'v': self.query,
                'prompt': self.prompt,
                'answer': self.answer}
