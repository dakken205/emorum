# -*- coding: utf-8 -*-

import datetime
import os
import typing as t

import dotenv
import sqlalchemy
import sqlalchemy.orm as orm

dotenv.load_dotenv()  # type: ignore


class Base(orm.DeclarativeBase):
    pass


class UserSerialized(t.TypedDict):
    id: str
    name: str
    password: str
    created_at: datetime.datetime


class User(Base):
    __tablename__ = "users"

    id: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    password: orm.Mapped[str]
    created_at: orm.Mapped[datetime.datetime]

    def serialize(
        self,
    ) -> UserSerialized:
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"


class PostSerialized(t.TypedDict):
    id: int
    author_id: str
    content: str
    emotion_value: float
    emotion_label: str
    color: str
    sender_addr: str
    created_at: datetime.datetime


class Post(Base):
    __tablename__ = "posts"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    author_id: orm.Mapped[str]
    content: orm.Mapped[str]
    emotion_value: orm.Mapped[float]
    emotion_label: orm.Mapped[str]
    color: orm.Mapped[str]
    sender_addr: orm.Mapped[str]
    created_at: orm.Mapped[datetime.datetime]

    def serialize(
        self,
    ) -> PostSerialized:
        return {
            "id": self.id,
            "author_id": self.author_id,
            "content": self.content,
            "emotion_value": self.emotion_value,
            "emotion_label": self.emotion_label,
            "color": self.color,
            "sender_addr": self.sender_addr,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, content={self.content})>"


engine = sqlalchemy.create_engine(os.environ["DATABASE_URI"])
Base.metadata.create_all(engine)
