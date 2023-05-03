"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    matches = relationship("Match", back_populates="user")

    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username

class Match(Base):
    __tablename__ = "matches"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.username"), nullable=False)
    opponent = Column("opponent", TEXT, nullable=False)
    score = Column("score", TEXT, nullable=False)
    date = Column("date", TEXT, nullable=False)
    notes = Column("notes", TEXT, nullable=False)
    
    user = relationship("User", back_populates="matches")

    # Constructor
    def __init__(self, user_id, opponent, score, date, notes):
        # id auto-increments
        self.user_id = user_id
        self.opponent = opponent
        self.score = score
        self.date = date
        self.notes = notes