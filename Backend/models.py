from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class SenseTagLink(SQLModel, table=True):
    sense_id: Optional[int] = Field(default=None, foreign_key="sense.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class KanjiTagLink(SQLModel, table=True):
    kanji_id: Optional[int] = Field(default=None, foreign_key="kanji.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class KanaTagLink(SQLModel, table=True):
    kana_id: Optional[int] = Field(default=None, foreign_key="kana.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class KanjiKanaSenseLink(SQLModel, table=True):
    kanji_id: Optional[int] = Field(default=None, foreign_key="kanji.id", primary_key=True)
    kana_id: Optional[int] = Field(default=None, foreign_key="kana.id", primary_key=True)
    sense_id: Optional[int] = Field(default=None, foreign_key="sense.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    definition: str
    kanji: List["Kanji"] = Relationship(back_populates="tags", link_model=KanjiTagLink)
    kana: List["Kana"] = Relationship(back_populates="tags", link_model=KanaTagLink)
    sense: List["Sense"] = Relationship(back_populates="tags", link_model=SenseTagLink)


class Kanji(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kanji")
    tags: List["Tag"] = Relationship(back_populates="kanji", link_model=KanjiTagLink)
    kanji_kana_link: List["Kana"] = Relationship(back_populates="kana_kanji_link", link_model=KanjiKanaSenseLink)
    kanji_sense_link: List["Sense"] = Relationship(back_populates="sense_kanji_link", link_model=KanjiKanaSenseLink)


class Kana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    common: bool = Field(default=False)
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="kana")
    tags: List[Tag] = Relationship(back_populates="kana", link_model=KanaTagLink)
    kana_kanji_link: List[Kanji] = Relationship(back_populates="kanji_kana_link", link_model=KanjiKanaSenseLink)
    kana_sense_link: List["Sense"] = Relationship(back_populates="sense_kana_link", link_model=KanjiKanaSenseLink)


class Sense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tags: List[Tag] = Relationship(back_populates="sense", link_model=SenseTagLink)
    related: Optional[str]
    antonym: Optional[str]
    field: Optional[str]
    dialect: Optional[str]
    misc: Optional[str]
    info: Optional[str]
    language_source: Optional[str]
    entry_id: Optional[int] = Field(foreign_key="entry.id", index=True)
    entry: Optional["Entry"] = Relationship(back_populates="sense")
    sense_kanji_link: List[Kanji] = Relationship(back_populates="kanji_sense_link", link_model=KanjiKanaSenseLink)
    sense_kana_link: List[Kana] = Relationship(back_populates="kana_sense_link", link_model=KanjiKanaSenseLink)
    examples: List["Example"] = Relationship(back_populates="sense")
    glosses: List["Gloss"] = Relationship(back_populates="sense")


class Example(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: Optional[str]
    sentence: Optional[str]
    translation: Optional[str]
    sense_id: Optional[int] = Field(foreign_key="sense.id", index=True)
    sense: Optional[Sense] = Relationship(back_populates="examples")


class Gloss(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lang: Optional[str]
    gender: Optional[str]
    type: Optional[str]
    text: str
    sense_id: Optional[int] = Field(foreign_key="sense.id", index=True)
    sense: Optional[Sense] = Relationship(back_populates="glosses")


class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(index=True, unique=True)
    kanji: List[Kanji] = Relationship(back_populates="entry")
    kana: List[Kana] = Relationship(back_populates="entry")
    sense: List[Sense] = Relationship(back_populates="entry")
