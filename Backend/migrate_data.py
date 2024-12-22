import json
from models import Kanji, Kana, Sense, Tag, KanjiTagLink, Entry
from sqlmodel import create_engine, SQLModel, Session, select
import os
from dotenv import load_dotenv

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_engine(postgres_url)

with open("JMdict.json", "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)


def create_tags():
    with Session(engine) as session:
        for tag_name, tag_definition in jmdict_data['tags'].items():
            statement = select(Tag).where(Tag.name == tag_name)
            existing_tag = session.exec(statement).first()  # type: ignore
            if not existing_tag:
                new_tag = Tag(name=tag_name, definition=tag_definition) # create new tag in the db
                session.add(new_tag)

        session.commit()
        print("Tags created successfully.")


def create_kanji():
    counter = 0
    session = Session(engine)

    for entry in jmdict_data['words']:
        entry_id = entry['id']
        entry_statement = select(Entry).where(Entry.entry_id == entry_id)
        existing_entry = session.exec(entry_statement).first()  # type: ignore
        if not existing_entry:    # create new entry in the db
            new_entry = Entry(entry_id=entry_id)
            session.add(new_entry)
            session.flush()
            existing_entry = new_entry

        for kanji in entry['kanji']:
            kanji_text= kanji['text']
            kanji_common = kanji['common']
            kanji_tags = kanji['tags']
            new_kanji = Kanji(text=kanji_text, common=kanji_common, entry_id=existing_entry.id)
            session.add(new_kanji)
            session.flush()
            for tag_name in kanji_tags:
                kanji_statement = select(Tag).where(Tag.name == tag_name)
                tag_res = session.exec(kanji_statement).first()  # type: ignore
                if tag_res:
                    new_kanji_tag_link = KanjiTagLink(kanji_id = new_kanji.id, tag_id = tag_res.id)
                    session.add(new_kanji_tag_link)

        counter += 1
        if counter >= 100:
            session.commit()
            break

create_tags()
create_kanji()