import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import html as hhtml
import requests
from urllib.parse import urlparse
import pandas as pd
import re

###
URL = 'https://globalsportsarchive.com/en/soccer/leagues'

def get_html(url):
    opt = Options()
    opt.add_argument('--headless=new')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(options=opt)
    try:
        driver.get(url)
        time.sleep(0.1)
        html = driver.page_source
        return html
    finally:
        driver.quit()

def get_html(url) -> str:
    opt = Options()
    opt.add_argument('--headless=new')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(options=opt)
    try:
        driver.get(url)
        time.sleep(0.1)
        html = driver.page_source
        return html
    finally:
        driver.quit()



###
soup = BeautifulSoup(get_html(URL), 'html.parser')
items = []
for item in soup.select(".gsa-comp-league-list .gsa-comp-league-list__item"):
    name_a = item.select_one(".gsa-comp-league-list__item-name a")
    img    = item.select_one(".gsa-comp-league-list__item-avatar img")
    items.append({
        "name": (name_a.get_text(strip=True) if name_a else None),
        "href": (name_a["href"] if name_a and name_a.has_attr("href") else None),
      })

top5 = items[1:6]
top5.append(next(x for x in items if "liga-portugal" in x["href"].lower()))

items = top5
###

pages = []
for liga in items:
    url = liga["href"]
    page = requests.get(url)
    pages.append(page)

###

def parse_gsa_matches(html: str, df: pd.DataFrame, league_name: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    for mat in soup.select(
    ".gsa-soccer-competition-rounds__item-content__sub_rounds > div.gsa-d-sm-md-none"
):
        a = soup.select_one("a.gsa-match-rounds-v2__match")
        date = a.select_one("p.gsa-match-rounds-v2__match-clock").get_text(strip=True)
        home = a.select_one(".gsa-flex-center.gsa-w-full").selecte_one(".gsa-flex-1:nth-of-type(1)").select_one(".gsa-d-sm-md-none.gsa-d-block").get_text(strip=True)
        print(a, date, home)


    return df

def parse_gsa_matches(html_text: str, df: pd.DataFrame, league_name: str, season: str):
    soup = BeautifulSoup(html_text, "html.parser")

    # Используем только desktop версию для избежания дублирования
    desktop_cards = soup.select("div.gsa-d-sm-md-block a.gsa-match-rounds__match")

    for card in desktop_cards:
        url = card.get("href", "")

        # Извлекаем match_id из URL
        match_id_match = re.search(r"/(\d+)$", url)
        match_id = match_id_match.group(1) if match_id_match else None

        if not match_id:
            continue

        # ===== Дата и время =====
        date_block = card.select_one(".gsa-match-rounds__match-info__date")
        date_str = None
        if date_block:
            date_parts = date_block.find_all("p")
            if len(date_parts) >= 2:
                date_part = date_parts[0].get_text(strip=True)  # "24.10"
                time_part = date_parts[1].get_text(strip=True)  # "21:00"
                year_match = re.search(r"/(\d{4})-\d{2}-\d{2}/", url)
                year = year_match.group(1) if year_match else "2025"
                date_str = f"{date_part}.{year}"

        # ===== Команды и счет =====
        home_team_block = card.select_one(".gsa-match-team.gsa-team-a")
        away_team_block = card.select_one(".gsa-match-team.gsa-team-b")

        def parse_team_data(team_block):
            """Парсим данные команды из блока"""
            if not team_block:
                return None, None, None

            # Полное и короткое название
            full_name = team_block.select_one(".gsa-d-sm-md-none.gsa-d-block")
            short_name = team_block.select_one(".gsa-d-sm-md-block.gsa-d-none")
            team_name = full_name.get_text(strip=True) if full_name else (
                short_name.get_text(strip=True) if short_name else None
            )

            # Счет
            score_el = team_block.select_one(".gsa-match-team__details-total")
            score = int(score_el.get_text(strip=True)) if score_el and score_el.get_text(strip=True).isdigit() else None

            # Результат (win/lose)
            symbol_el = team_block.select_one(".gsa-match-team__details-symbol")
            result = symbol_el.get_text(strip=True).lower() if symbol_el else None
            if result == "w":
                result = "win"
            elif result == "l":
                result = "lose"

            return team_name, score, result

        home_name, home_score, home_result = parse_team_data(home_team_block)
        away_name, away_score, away_result = parse_team_data(away_team_block)

        # Определяем результат, если нет символов
        if home_score is not None and away_score is not None:
            if home_result is None and away_result is None:
                if home_score > away_score:
                    home_result, away_result = "win", "lose"
                elif home_score < away_score:
                    home_result, away_result = "lose", "win"
                else:
                    home_result = away_result = "draw"

        if not all([home_name, away_name, match_id]):
            continue

        # ===== Добавляем в DataFrame =====
        df.loc[len(df)] = [
            home_name, match_id, home_score, away_name, home_result,
            "home", league_name, date_str, season  # 👈 добавили сезон
        ]
        df.loc[len(df)] = [
            away_name, match_id, away_score, home_name, away_result,
            "away", league_name, date_str, season  # 👈 добавили сезон
        ]

    return df

COOKIES_PATH = "cookies_gsa.json"
df = pd.DataFrame(columns=["team", "match_id", "pts", "opponent", "result", "home_away", "league", "date", "season"])

# ===================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====================

def save_cookies_to_file(sess: requests.Session, path: str = COOKIES_PATH):
    data = requests.utils.dict_from_cookiejar(sess.cookies)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_cookies_from_file(sess: requests.Session, path: str = COOKIES_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sess.cookies = requests.utils.cookiejar_from_dict(data, cookiejar=None, overwrite=True)
    except FileNotFoundError:
        pass

def make_session(base_url: str, referer: str) -> requests.Session:
    s = requests.Session()
    load_cookies_from_file(s)
    s.headers.update({
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "KHTML, like Gecko) Chrome/125 Safari/537.36"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": referer,
        "Origin": f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}",
    })
    return s

def extract_csrf(soup: BeautifulSoup):
    tag = soup.find("meta", attrs={"name": "csrf-token"})
    return tag["content"] if tag and tag.has_attr("content") else None

def seasons_dict(soup):
    pairs = {}

    # 1️⃣ Сначала ищем <a> со ссылками (самый точный способ)
    for a in soup.select("a[href*='/competition/']"):
        href = a.get("href", "")
        txt = a.get_text(" ", strip=True)
        if re.search(r"\d{4}\s*/\s*\d{4}", txt) and "/competition/" in href:
            # нормализуем ключ (2022/2023)
            key = re.sub(r"\s+", "", txt)
            pairs[key] = href

    # 2️⃣ fallback: если не нашли ссылок, пробуем <option>
    if not pairs:
        for opt in soup.select("select.gsa-comp-select > option"):
            sid = opt.get("value")
            txt = opt.get_text(" ", strip=True)
            if sid and re.search(r"\d{4}\s*/\s*\d{4}", txt):
                key = re.sub(r"\s+", "", txt)
                pairs[key] = sid  # ID как раньше

    return pairs

# ===================== ОСНОВНОЙ ЦИКЛ =====================

count = 0

for liga in items:
    url = liga["href"]
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    sess = make_session(base, referer=url)

    # загружаем основную страницу
    page = sess.get(url, timeout=30)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    get_ids = seasons_dict(soup)

    # если ничего не нашли — пробуем /seasons
    if not get_ids:
        alt_url = url.rstrip("/") + "/seasons"
        try:
            alt_page = sess.get(alt_url, timeout=30)
            alt_page.raise_for_status()
            soup_alt = BeautifulSoup(alt_page.text, "html.parser")
            get_ids = seasons_dict(soup_alt)
            print(f"[+] Переключились на страницу сезонов: {alt_url}")
        except Exception as e:
            print(f"[!] Не удалось загрузить сезоны для {url}: {e}")
            get_ids = {}

    print(f"{liga['name']} — найдено {len(get_ids)} сезонов")

    for year in ("2021-2022", "2022-2023", "2023-2024", "2024-2025"):
        year_key = year.replace("-", "/")
        season_entry = get_ids.get(year_key)

        if not season_entry:
            print(f"[!] Нет сезона {year} в get_ids для {liga['name']}. Доступные ключи:", list(get_ids.keys()))
            continue

        # если в словаре уже есть полный href — используем его напрямую
        if "/competition/" in season_entry:
            if not season_entry.startswith("http"):
                year_url = f"{base}{season_entry}"
            else:
                year_url = season_entry
            # извлекаем ID сезона из конца URL (после последнего /)
            season_id = re.search(r"/(\d+)/?$", year_url)
            season_id = season_id.group(1) if season_id else None
        else:
            # fallback, если сохранился только ID
            season_id = season_entry
            year_url = re.sub(r"-\d{4}-\d{4}/\d+$", f"-{year}/{season_id}", url)

        # загружаем страницу сезона
        page = sess.get(year_url, timeout=30)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        csrf = extract_csrf(soup)
        cal = soup.select_one(".gsa-comp-calendar.gsa-border-top")
        dates_raw = cal.get("data-weeks") if cal else None
        if not dates_raw:
            print(f"[!] data-weeks не найдено для {liga['name']} ({year})")
            continue

        weeks = json.loads(hhtml.unescape(dates_raw)).keys()
        url_widget = f"{base}/en/widget/match_competition_round_gameweek"

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        if csrf:
            headers["X-CSRF-Token"] = csrf

        for week in weeks:
            payload = {
                "sport": "soccer",
                "roundKey": week.split("_")[0],
                "activeSubRoundKey": week,
                "isActiveRound": "",
                "competitionId": season_id,  # теперь корректно
            }
            resp = sess.post(url_widget, data=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            count += 1
            df = parse_gsa_matches(resp.text, df, league_name=liga["name"], season=year)

        save_cookies_to_file(sess)
        print(f"[+] {liga['name']} — сезон {year} успешно обработан")


print(df)
df.to_csv("matches_dataset.csv", index=False, encoding="utf-8-sig")