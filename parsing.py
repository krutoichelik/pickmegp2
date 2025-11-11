from common import *

###
URL = 'https://globalsportsarchive.com/en/soccer/leagues'

"""
здесь функция для того, чтобы использовать селениум драйвер
для загрузки страниц для загрузки страниц (чтобы подгружались динамические элементы)
возвращать будет html код страницы
"""
def get_html(url):
    opt = Options()
    opt.add_argument('--headless=new') #создаётся объект options — это настройки браузера (для гулг хром)
    opt.add_argument('--no-sandbox') #фоновый режим гугла, отключает механизм безопасности sandbox
    opt.add_argument('--disable-dev-shm-usage') #отключает использование специальной памяти linux
    driver = webdriver.Chrome(options=opt) #создает драйвер - браузер, которым управляет питон
    driver.get(url) #получаем ссылку
    time.sleep(0.1) #чтобы страница успела загрузиться
    html = driver.page_source #получаем код страницы, то что загружается через java-script
    return html


"""
используем бьютифул суп, который создает объект для анализа, 
для того, чтобы парсить html 
берем получившийся код страницы
изучив сайт, понимаем, что лиги хранятся в таком формате, находим все элементы
.gsa-comp-league-list__item.
берем имя лиги и ссылку на страницу лиги - все сохраняем в список items
"""

soup = BeautifulSoup(get_html(URL), 'html.parser')
items = []
for item in soup.select(".gsa-comp-league-list .gsa-comp-league-list__item"):
    # soup.select - ищет все html- элементы, соответсвующие сss пути
    name_a = item.select_one(".gsa-comp-league-list__item-name a")
    #хранится html тег
    items.append({ #формируем название и ссылку из тега
        "name": (name_a.get_text(strip=True) if name_a else None),
        "href": (name_a["href"] if name_a and name_a.has_attr("href") else None),
    })

#выбираем лиги, берем с ссылки сайта
chosen_leagues = items[1:6]
#отдельно тут ищем португалию, она не в начале
for x in items:
    if x["href"] and "liga-portugal" in x["href"].lower():
        chosen_leagues.append(x)
        break

items = chosen_leagues #cловарик лиг

#проверяем работу страниц
pages = []
for liga in items:
    url = liga["href"]
    page = requests.get(url)
    """
     с помощью библиотеки риквестс
     мы делаем запрос на http
     возвращается объект response, который содержит типо код
     нап (200) - все ок
     html текст страницы 
     и page.url крч реальная ссылка
    """
    pages.append(page)


"""
функция извлекает все матчи из HTML одной игровой недели
находит все ссылки на матчи (a.gsa-match-rounds__match).
id матча (через re.search в URL), дату и год сезона,названия команд, счёт, результат
"""


def parse_gsa_matches(html_text, df, league_name, season):
    #код страницы, куда добавляем матчи, имя лиги, сезон
    soup = BeautifulSoup(html_text, "html.parser")
#опять создаем объект
    for card in soup.select("div.gsa-d-sm-md-block a.gsa-match-rounds__match"):
    #ищем все карточки матчей - ссылки с данными о них
        url = card.get("href", "")
        #ссылка на конкретный матч
        # Извлекаем match_id
        match_id_match = re.search(r"/(\d+)$", url) #регулярное выражение, где на конце цифры - их берем
        match_id = match_id_match.group(1) if match_id_match else None
        #.group(1) возвращает текст, найденный внутри первой скобочной группы в шаблоне регулярного выражения
        if not match_id:
            continue
        #если нет айдишки - скип

        # парсим дату
        date_block = card.select_one(".gsa-match-rounds__match-info__date")
        #ищем вот такую строчку, если нет - нан
        date_str = None
        if date_block:
            #разбираем ее подробно
            #ишем <p> находит абзацы, там все хранится отдельно, разбиваем на части
            date_parts = date_block.find_all("p")
            if len(date_parts) >= 2:
                date_part = date_parts[0].get_text(strip=True)
                year_match = re.search(r"/(\d{4})-\d{2}-\d{2}/", url)
                year = year_match.group(1) if year_match else "2025"
                date_str = f"{date_part}.{year}"


        #вносим команду а и b
        home_team_block = card.select_one(".gsa-match-team.gsa-team-a")
        away_team_block = card.select_one(".gsa-match-team.gsa-team-b")

        #вложенная функция, где обрабатываем команду - ее имя, счет и результат
        def parse_team_data(team_block):
            full_name = team_block.select_one(".gsa-d-sm-md-none.gsa-d-block")
            short_name = team_block.select_one(".gsa-d-sm-md-block.gsa-d-none")
            team_name = full_name.get_text(strip=True) if full_name else (
                short_name.get_text(strip=True) if short_name else None
            )

            # счет
            score_el = team_block.select_one(".gsa-match-team__details-total")
            score = int(score_el.get_text(strip=True)) if score_el and score_el.get_text(strip=True).isdigit() else None
            #get_text() возвращает всё содержимое между тегами в виде строки
            #strip=True удаляет все пробелы и переносы строк по краям
            #.isdigit() проверяет, состоит ли строка только из цифр

            # результат
            symbol_el = team_block.select_one(".gsa-match-team__details-symbol")
            result = symbol_el.get_text(strip=True).lower() if symbol_el else None
            if result == "w":
                result = "win"
            elif result == "l":
                result = "lose"

            return team_name, score, result

        home_name, home_score, home_result = parse_team_data(home_team_block)
        away_name, away_score, away_result = parse_team_data(away_team_block)

        # определяем результат, если нет символов
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

        #добавляем в датафрейм
        df.loc[len(df)] = [
            home_name, match_id, home_score, away_name, home_result,
            "home", league_name, date_str, season
        ]
        df.loc[len(df)] = [
            away_name, match_id, away_score, home_name, away_result,
            "away", league_name, date_str, season
        ]

    return df

"""
это глобальная переменная, в которой хранится путь файла, где будут сохраняться cookies
если потом снова обращаешься к сайту и передаёшь эти cookies обратно —
сайт помнит тебя
"""
COOKIES_PATH = "cookies_gsa.json"
df = pd.DataFrame(columns=["team", "match_id", "pts", "opponent", "result", "home_away", "league", "date", "season"])


#немного функций для упрощения мейна

"""
функция сохраняет кукисы из текущей сессии
sess — это объект типа requests.Session(),
внутри него хранятся все текущие cookies

path — путь к файлу, куда сохраняем cookies (по умолчанию "cookies_gsa.json")
"""
def save_cookies_to_file(sess: requests.Session, path: str = COOKIES_PATH):
    data = requests.utils.dict_from_cookiejar(sess.cookies)
    #преобразовываем в питон словарь, чтобы удобнее было
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    #если файл существует - перезапишется, открывается или создается в режиме записи


"""
эта функция наоборот восстанавливает парсер 
чтобы драйвер пониал, что это мы
"""
def load_cookies_from_file(sess: requests.Session, path: str = COOKIES_PATH):
    try: #может быть ошибка, если файла еще нет, поэтому чтобы если что не было ошибки
        with open(path, "r", encoding="utf-8") as f:
            #открываем файл в режиме чтения
            data = json.load(f) #достаем все джсон из файла
        sess.cookies = requests.utils.cookiejar_from_dict(data, cookiejar=None, overwrite=True)
        # превращаем в словарь - контейнер для куки
    except FileNotFoundError: #если его нет - то прсото скипаем
        pass

""" 
создаём HTTP-сессию с нужными заголовками и загруженными cookies, 
чтобы парсер выглядел как настоящий браузер и не ловил блокировки
"""
def make_session(base_url: str, referer: str) -> requests.Session:
    #base_url - основной адрес сайта, referer - страница с которой мы переходим
    s = requests.Session()
    #создаем сессию - хранит куки файлы, заголовки, соединения
    load_cookies_from_file(s) #функция выше
    #эти заголовки нам нужны, чтобы браузер воспринимало нас как пользователя
    s.headers.update({
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "KHTML, like Gecko) Chrome/125 Safari/537.36"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": referer,
        "Origin": f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}",
    })
    return s

"""
она достаёт CSRF-токен (анти-взломный ключ) со страницы, 
чтобы парсер мог успешно отправлять POST-запросы
"""
def extract_csrf(soup):
    tag = soup.find("meta", attrs={"name": "csrf-token"})
    #ищем первый элемент, соответсвующий условиям
    return tag["content"] if tag and tag.has_attr("content") else None
    #возвращаем токен

"""
находит список сезонов (2021/2022, 2022/2023 и т.д.) на странице лиги и возвращает их в виде словаря:
где ключ — название сезона, а значение — ссылка или ID этого сезона
"""

def seasons_dict(soup):
    pairs = {}

    # сначала ищем <a> со ссылками (самый точный способ)
    for a in soup.select("a[href*='/competition/']"):
        href = a.get("href", "")
        txt = a.get_text(" ", strip=True)
        if re.search(r"\d{4}\s*/\s*\d{4}", txt) and "/competition/" in href: #проверяем действительно ли это сезон
            # нормализуем ключ (2022/2023)
            key = re.sub(r"\s+", "", txt)
            pairs[key] = href

    # если не нашли ссылок, пробуем <option>
    if not pairs:
        for opt in soup.select("select.gsa-comp-select > option"):
            sid = opt.get("value")
            txt = opt.get_text(" ", strip=True)
            if sid and re.search(r"\d{4}\s*/\s*\d{4}", txt):
                key = re.sub(r"\s+", "", txt)
                pairs[key] = sid  # ID как раньше

    return pairs #словарь сезонов

count = 0 #счетчик обработанных недель
for liga in tqdm(items):
    """
    проходим по списку items, где лежат данные о всех выбранных лигах.
    tqdm — это просто прогресс-бар, чтобы видно было, как идёт парсинг
    """

    #извлекаем страницу текущей лиги
    url = liga["href"]
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    sess = make_session(base, referer=url)

    # загружаем основную страницу, проверяем, что сервер ответил 200
    page = sess.get(url, timeout=30)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    get_ids = seasons_dict(soup) #достаем словарь сезонов

    # если ничего не нашли — пробуем /seasons - если они лежат не на главной
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

    #перебираем все нужные сезоны по лигам
    for year in ("2021-2022", "2022-2023", "2023-2024", "2024-2025"):
        year_key = year.replace("-", "/")
        season_entry = get_ids.get(year_key)

        if not season_entry:
            print(f"[!] Нет сезона {year} в get_ids для {liga['name']}. Доступные ключи:", list(get_ids.keys()))
            continue

        # определяем ссылку сезона
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

        #достаём CSRF-токен и блок календаря
        csrf = extract_csrf(soup)
        cal = soup.select_one(".gsa-comp-calendar.gsa-border-top")
        dates_raw = cal.get("data-weeks") if cal else None
        #data-weeks — специальный атрибут с JSON-списком недель
        if not dates_raw: #если  нет - скип
            print(f"[!] data-weeks не найдено для {liga['name']} ({year})")
            continue

        """
        hhtml.unescape() — превращает HTML-encoded JSON обратно в нормальный
	    json.loads() — загружает JSON в Python-словарь
	    .keys() — получаем список всех игровых недель
        """
        weeks = json.loads(hhtml.unescape(dates_raw)).keys()
        url_widget = f"{base}/en/widget/match_competition_round_gameweek"
        #AJAX-эндпоинт, который сайт использует, чтобы динамически подгружать матчи каждой недели
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        if csrf:
            headers["X-CSRF-Token"] = csrf

        #перебираем недели
        for week in weeks:
            """
            словарь с параметрами, которые сайт ожидает получить при AJAX-запросе
            он имитирует поведение JavaScript на странице, 
            когда пользователь выбирает нужную неделю в календаре
            """
            payload = {
                "sport": "soccer",
                "roundKey": week.split("_")[0],
                "activeSubRoundKey": week,
                "isActiveRound": "",
                "competitionId": season_id,  # теперь корректно
            }
            resp = sess.post(url_widget, data=payload, headers=headers, timeout=30) #отправляем запрос на сервер
            resp.raise_for_status() #проверяем на сбой
            count += 1
            df = parse_gsa_matches(resp.text, df, league_name=liga["name"], season=year)
            #html код недели - все данные о матчах

        save_cookies_to_file(sess)
        print(f"[+] {liga['name']} — сезон {year} успешно обработан")

print(df)
df.to_csv("matches_dataset.csv", index=False, encoding="utf-8-sig")
