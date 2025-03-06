import requests
from bs4 import BeautifulSoup
import time
import json


def scrape_kanji_for_level(level):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    kanji_data = []
    page_num = 1

    while True:
        if page_num == 1:
            url = f"https://jisho.org/search/%23jlpt-{level}%20%23kanji"
        else:
            url = f"https://jisho.org/search/%23jlpt-{level}%20%23kanji?page={page_num}"

        try:
            response = requests.get(url, headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            entries = soup.find_all("div", class_="kanji_light_content")

            if not entries:
                print(f"No more entries found for JLPT {level}")
                break

            for entry in entries:
                kanji = entry.find("span", class_="character literal japanese_gothic")
                kanji_text = kanji.get_text(strip=True) if kanji else None

                meanings_div = entry.find("div", class_="meanings english sense")
                meanings_text = [span.get_text(strip=True) for span in meanings_div.find_all("span")] if meanings_div else []

                kun_readings_div = entry.find("div", class_="kun readings")
                kun_readings_text = [a.get_text(strip=True) for a in kun_readings_div.find_all("a")] if kun_readings_div else []

                on_readings_div = entry.find("div", class_="on readings")
                on_readings_text = [a.get_text(strip=True) for a in on_readings_div.find_all("a")] if on_readings_div else []

                kanji_data.append({
                    'kanji': kanji_text,
                    'meanings': ', '.join(meanings_text).replace(',,', ','),
                    'kun_readings': ', '.join(kun_readings_text),
                    'on_readings': ', '.join(on_readings_text),
                    'jlpt_level': level
                })


            print(f"Scraped page {page_num} for JLPT {level}")

            page_num += 1

            time.sleep(10)

        except requests.RequestException as e:
            print(f"Error scraping page {page_num} for JLPT {level}: {e}")
            break

    return kanji_data


def scrape_all_levels():
    jlpt_levels = ["n5", "n4", "n3", "n2", "n1"]
    all_kanji_data = []
    for level in jlpt_levels:
        print(f"Starting scraping for JLPT {level}")
        level_kanji_data = scrape_kanji_for_level(level)
        all_kanji_data.extend(level_kanji_data)
        print(f"Total Kanji found for JLPT {level}: {len(level_kanji_data)}")

    return all_kanji_data


all_kanji_data = scrape_all_levels()
with open("kanji_data.json", "w", encoding="utf-8") as json_file:
    json.dump(all_kanji_data, json_file, ensure_ascii=False, indent=4)




