from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.common.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    content = Column(String(1000))
    hashtags = relationship("Hashtag", secondary="post_hashtag", back_populates="posts")

    def __init__(self, title, content):
        self.title = title
        self.content = content


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False, unique=True)
    posts = relationship("Post", secondary="post_hashtag", back_populates="hashtags")

    def __init__(self, title):
        self.title = title


class PostHashtag(Base):
    __tablename__ = "post_hashtag"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    hashtag_id = Column(Integer, ForeignKey("hashtags.id"))