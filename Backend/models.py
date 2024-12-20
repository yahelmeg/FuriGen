from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Kanji(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kanji")

class Kana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kana")

class Sense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="sense")

class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: str = Field(index=True, unique=True)
    kanji: List[Kanji] = Relationship(back_populates="entry")
    kana: List[Kana] = Relationship(back_populates="entry")
    sense: List[Sense] = Relationship(back_populates="entry")