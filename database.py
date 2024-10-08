from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

Base = declarative_base()
Base:declarative_base

class Debate(Base):
    __tablename__ = "debates"

    vote_id = Column(Integer,  ForeignKey('laws.vote_id'), primary_key=True)
    session_id = Column(Integer, nullable=False)
    sitting_id = Column(Integer, nullable=False)
    debate_id = Column(Integer, unique=True)
    debate_no = Column(Text, nullable=False)
    debate_name = Column(Text, nullable=False)
    document_link = Column(Text, nullable=False)
    download_link = Column(Text, nullable=False)
    filename = Column(Text, nullable=False)

    votes = relationship("Vote", back_populates="debate")
    law = relationship("Law", back_populates="debate", uselist=False)

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    nominating_party = Column(Text, nullable=False)
    group = Column(Text, nullable=False)

    votes = relationship("Vote", back_populates="member")

class Vote(Base):
    __tablename__ = "votes"

    vote_id = Column(Integer, ForeignKey('debates.vote_id'), ForeignKey('laws.vote_id'), primary_key=True)
    member_id = Column(Integer, ForeignKey('members.member_id'), primary_key=True)
    vote = Column(Integer, nullable=False)

    debate = relationship("Debate", back_populates="votes")
    member = relationship("Member", back_populates="votes")
    law = relationship("Law", back_populates="votes")

class Law(Base):
    __tablename__ = "laws"

    vote_id = Column(Integer, primary_key=True)
    document_category = Column(Text)
    document_summary = Column(Text)
    document_importance_score = Column(Text)

    debate = relationship("Debate", back_populates="law", uselist=False)
    votes = relationship("Vote", back_populates="law")

# -- Create debates table
# CREATE TABLE debates (
#     vote_id INTEGER PRIMARY KEY,
#     session_id INTEGER NOT NULL,
#     sitting_id INTEGER NOT NULL,
#     debate_id INTEGER NOT NULL,
#     debate_no TEXT NOT NULL,
#     debate_name TEXT NOT NULL,
#     document_link TEXT NOT NULL,
#     download_link TEXT NOT NULL,
#     filename TEXT NOT NULL
# );
#
# -- Create members table
# CREATE TABLE members (
#     member_id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     surname TEXT NOT NULL,
#     nominating_party TEXT NOT NULL,
#     "group" TEXT NOT NULL
# );
#
# -- Create laws table
# CREATE TABLE laws (
#     vote_id INTEGER PRIMARY KEY,
#     document_category TEXT,
#     document_summary TEXT,
#     document_importance_score TEXT
# );
#
# -- Create votes table
# CREATE TABLE votes (
#     vote_id INTEGER,
#     member_id INTEGER,
#     vote INTEGER NOT NULL,
#     PRIMARY KEY (vote_id, member_id),
#     FOREIGN KEY (vote_id) REFERENCES laws (vote_id),
#     FOREIGN KEY (vote_id) REFERENCES debates (vote_id),
#     FOREIGN KEY (member_id) REFERENCES members(member_id)
# );
#
# -- Add foreign key to debates table referencing laws
# ALTER TABLE debates
# ADD CONSTRAINT fk_debates_laws
# FOREIGN KEY (vote_id) REFERENCES laws(vote_id);