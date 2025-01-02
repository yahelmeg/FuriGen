from sqlalchemy.orm import Session
from Backend.Database.database import engine
from Backend.Database.entities import Kanji, Kana, Sense, Example, Gloss, Tag, KanjiKanaLink, KanjiSenseLink, SenseTagLink
from .kanji_response_models import *
from sqlmodel import select
from fastapi import APIRouter

router = APIRouter(prefix="/kanji")

@router.get("/kana", response_model=list[KanaResponse])
def get_kana_for_kanji(kanji: str):
    res = []
    session = Session(engine)
    statement = select(Kanji).where(Kanji.text == kanji)
    kanji_list = session.execute(statement).scalars().all()
    for kanji in kanji_list:
        statement = select(KanjiKanaLink).where(KanjiKanaLink.kanji_id == kanji.id)
        kanji_kana_link_list = session.execute(statement).scalars().all()
        for link in kanji_kana_link_list:
            statement = select(Kana).where(Kana.id == link.kana_id)
            kana_list = session.execute(statement).scalars().all()
            for kana in kana_list:
                res.append(kana)
    return res

@router.get("/example", response_model=list[ExampleResponse])
def get_example_for_kanji(kanji: str):
    res = []
    session = Session(engine)
    statement = select(Kanji).where(Kanji.text == kanji)
    kanji_list = session.execute(statement).scalars().all()
    for kanji in kanji_list:
        statement = select(KanjiSenseLink).where(KanjiSenseLink.kanji_id == kanji.id)
        kanji_sense_link_list = session.execute(statement).scalars().all()
        for link in kanji_sense_link_list:
            statement = select(Sense).where(Sense.id == link.sense_id)
            sense_list = session.execute(statement).scalars().all()
            for sense in sense_list:
                statement = select(Example).where(Example.sense_id == sense.id)
                example_list = session.execute(statement).scalars().all()
                for example in example_list:
                    res.append(example)
    return res


@router.get("/gloss", response_model=list[GlossResponse])
def get_example_for_kanji(kanji: str):
    res = []
    session = Session(engine)
    statement = select(Kanji).where(Kanji.text == kanji)
    kanji_list = session.execute(statement).scalars().all()
    for kanji in kanji_list:
        statement = select(KanjiSenseLink).where(KanjiSenseLink.kanji_id == kanji.id)
        kanji_sense_link_list = session.execute(statement).scalars().all()
        for link in kanji_sense_link_list:
            statement = select(Sense).where(Sense.id == link.sense_id)
            sense_list = session.execute(statement).scalars().all()
            for sense in sense_list:
                statement = select(Gloss).where(Gloss.sense_id == sense.id)
                gloss_list = session.execute(statement).scalars().all()
                for gloss in gloss_list:
                    res.append(gloss)
    return res

@router.get("/partofspeech", response_model=list[TagResponse])
def get_part_of_speech_for_kanji(kanji: str):
    res = []
    session = Session(engine)
    statement = select(Kanji).where(Kanji.text == kanji)
    kanji_list = session.execute(statement).scalars().all()
    for kanji in kanji_list:
        statement = select(KanjiSenseLink).where(KanjiSenseLink.kanji_id == kanji.id)
        kanji_sense_link_list = session.execute(statement).scalars().all()
        for kanji_sense_link in kanji_sense_link_list:
            statement = select(Sense).where(Sense.id == kanji_sense_link.sense_id)
            sense_list = session.execute(statement).scalars().all()
            for sense in sense_list:
                statement = select(SenseTagLink).where(SenseTagLink.sense_id == sense.id)
                sense_tag_link_list = session.execute(statement).scalars().all()
                for sense_tag_link in sense_tag_link_list:
                    statement = select(Tag).where(Tag.id == sense_tag_link.tag_id)
                    tag_list = session.execute(statement).scalars().all()
                    for tag in tag_list:
                        if tag not in res:
                            res.append(tag)
    return res