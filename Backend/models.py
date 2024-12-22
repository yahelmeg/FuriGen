from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class KanjiTagLink(SQLModel, table=True):
    kanji_id: Optional[int] = Field(default=None, foreign_key="kanji.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class KanjiKanaLink(SQLModel, table=True):
    kanji_id: Optional[int] = Field(default=None, foreign_key="kanji.id", primary_key=True)
    kana_id: Optional[int] = Field(default=None, foreign_key="kana.id", primary_key=True)


class KanaTagLink(SQLModel, table=True):
    kana_id: Optional[int] = Field(default=None, foreign_key="kana.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    definition: str
    kanji: List["Kanji"] = Relationship(back_populates="tags", link_model=KanjiTagLink)
    kana: List["Kana"] = Relationship(back_populates="tags", link_model=KanaTagLink)


class Kanji(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kanji")
    tags: List["Tag"] = Relationship(back_populates="kanji", link_model=KanjiTagLink)
    kana: List["Kana"] = Relationship(back_populates="kanji", link_model=KanjiKanaLink)


class Kana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kana")
    kanji: List[Kanji] = Relationship(back_populates="kana", link_model=KanjiKanaLink)
    tags: List[Tag] = Relationship(back_populates="kana", link_model=KanaTagLink)


class Sense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="sense")


class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(index=True, unique=True)
    kanji: List[Kanji] = Relationship(back_populates="entry")
    kana: List[Kana] = Relationship(back_populates="entry")
    sense: List[Sense] = Relationship(back_populates="entry")