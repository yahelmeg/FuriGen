from sqlalchemy.orm import Session
from Backend.Database.database import  engine
from Backend.Database.entities import  Kanji, Kana, KanjiKanaLink
from sqlmodel import select
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/kana")

class KanjiResponse(BaseModel):
    text: str
    common: bool

@router.get("/kanji", response_model=list[KanjiResponse])
def get_kanji_for_kana(kana: str):
    res = []
    session = Session(engine)
    statement = select(Kana).where(Kana.text == kana)
    kana_list = session.execute(statement).scalars().all()
    for kana in kana_list:
        statement = select(KanjiKanaLink).where(KanjiKanaLink.kana_id == kana.id)
        kanji_kana_link_list = session.execute(statement).scalars().all()
        for link in kanji_kana_link_list:
            statement = select(Kanji).where(Kanji.id == link.kanji_id)
            kanji_list = session.execute(statement).scalars().all()
            for kanji in kanji_list:
                res.append(kanji)
    return res
