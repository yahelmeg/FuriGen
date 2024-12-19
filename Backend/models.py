from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Kanji(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    common: bool=False
    entry_id: Field(foreign_key="entry.id")
    entry: "Entry" = Relationship(back_populates="kanji")

class Kana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    common: bool=False
    entry_id: Field(foreign_key="entry.id")
    entry: "Entry" = Relationship(back_populates="kana")

class Sense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    common: bool=False
    entry_id: Field(foreign_key="entry.id")
    entry: "Entry" = Relationship(back_populates="sense")

class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id = str
    kanji: List[Kanji] = Relationship(back_populates="entry")
    kana: List[Kana] = Relationship(back_populates="entry")
    sense: List[Sense] = Relationship(back_populates="entry")


