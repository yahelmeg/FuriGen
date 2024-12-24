import json
from models import *
from sqlmodel import create_engine, SQLModel, Session, select
import os
from dotenv import load_dotenv
from tqdm import tqdm

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
    session = Session(engine)
    total_tags = len(jmdict_data['tags'])
    with tqdm(total=total_tags, desc="Processing Tags", unit=" Tag") as pbar:
        for tag_name, tag_definition in jmdict_data['tags'].items():
            statement = select(Tag).where(Tag.name == tag_name)
            existing_tag = session.exec(statement).first()  # type: ignore
            if not existing_tag:
                new_tag = Tag(name=tag_name, definition=tag_definition) # create new tag in the db
                session.add(new_tag)
                pbar.update(1)

        session.commit()
        pbar.close()

def create_entries():
    commit_counter = 0
    session = Session(engine)
    total_entries = len(jmdict_data['words'])
    with tqdm(total= total_entries, desc="Processing Entries", unit=" Entry") as pbar:
        for entry in jmdict_data['words']:
            entry_id = entry['id']
            entry_statement = select(Entry).where(Entry.entry_id == entry_id)
            existing_entry = session.exec(entry_statement).first()  # type: ignore
            if not existing_entry:    # create new entry in the db
                new_entry = Entry(entry_id=entry_id)
                session.add(new_entry)
                session.flush()
                existing_entry = new_entry

            #process kanji
            kanji_list = []
            for kanji in entry['kanji']:
                kanji_text= kanji['text']
                kanji_common = kanji['common']
                kanji_tags = kanji['tags']
                new_kanji = Kanji(text=kanji_text, common=kanji_common, entry_id=existing_entry.id)
                session.add(new_kanji)
                kanji_list.append(new_kanji)
                session.flush()
                for tag_name in kanji_tags:
                    search_tag_statement = select(Tag).where(Tag.name == tag_name)
                    tag_res = session.exec(search_tag_statement).first()  # type: ignore
                    if tag_res:
                        new_kanji_tag_link = KanjiTagLink(kanji_id = new_kanji.id, tag_id = tag_res.id)
                        session.add(new_kanji_tag_link)

            #process kana
            kana_list = []
            for kana in entry['kana']:
                kana_text = kana['text']
                kana_common = kana['common']
                kana_tags = kana['tags']
                new_kana = Kana(text=kana_text, common=kana_common, entry_id=existing_entry.id)
                session.add(new_kana)
                kana_list.append(new_kana)
                session.flush()
                for tag_name in kana_tags:
                    search_tag_statement = select(Tag).where(Tag.name == tag_name)
                    tag_res = session.exec(search_tag_statement).first()  # type: ignore
                    if tag_res:
                        new_kana_tag_link = KanaTagLink(kana_id=new_kana.id, tag_id=tag_res.id)
                        session.add(new_kana_tag_link)

            #process sense
            for sense in entry['sense']:
                sense_tags = sense['partOfSpeech']
                related = sense['related']
                antonym = sense['antonym']
                field = sense['field']
                dialect = sense['dialect']
                misc = sense['misc']
                info = sense['info']
                language_source = ", ".join(sense['languageSource'])
                new_sense = Sense(tag=sense_tags, related=related, antonym=antonym, field=field,
                                  dialect=dialect, misc=misc, info=info,
                                  language_source=language_source,  entry_id=existing_entry.id )
                session.add(new_sense)
                session.flush()
                for tag_name in sense_tags:
                    search_tag_statement = select(Tag).where(Tag.name == tag_name)
                    tag_res = session.exec(search_tag_statement).first()  # type: ignore
                    if tag_res:
                        new_sense_tag_link = SenseTagLink(sense_id=new_sense.id, tag_id=tag_res.id)
                        session.add(new_sense_tag_link)

                #process gloss
                for gloss in sense['gloss']:
                    gloss_text = gloss['text']
                    gloss_type = gloss['type']
                    gloss_gender = gloss['gender']
                    gloss_lang = gloss['lang']
                    new_gloss = Gloss(lang=gloss_lang, gender=gloss_gender,
                                      type=gloss_type, text=gloss_text, sense_id= sense.id)
                    session.add(new_gloss)
                    session.flush()

                #process example
                for example in sense['example']:
                    example_text = example['text']
                    example_sentence = example['sentences'][0].get('text', '')
                    example_translation = example['sentences'][1].get('text', '')
                    new_example = Example(text=example_text, sentence= example_sentence,
                                          translation = example_translation, sense_id= sense.id)
                    session.add(new_example)
                    session.flush()

            commit_counter += 1
            pbar.update(1)
            if commit_counter % 100 == 0: # commit every 100 entries
                session.commit()
        session.commit()
        pbar.close()

create_tags()
create_entries()

