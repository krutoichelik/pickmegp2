from bs4 import BeautifulSoup
from pathlib import Path
from pandas import DataFrame
import pandas as pd
import requests


def get_html_str(link: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "KHTML, like Gecko) Chrome/123 Safari/537.36"
        ),
        "Accept-Language": "ru,en;q=0.9",
    }
    r = requests.get(link, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def parse(link: str, df: DataFrame):
    soup = BeautifulSoup(
        get_html_str(link),
        "html.parser",
    )
    name = link.split("/")[-4].strip()

    table = soup.select_one("table")
    for line in table.select("tr.odd"):
        season, match_, soldout = (i.text for i in line.select(".zentriert"))
        audience, average = (i.text for i in line.select(".rechts"))
        liga = line.select_one(".links").text.strip()
        df.loc[len(df)] = {
            "Сезон": str(season).strip(),
            "Лига": str(liga).strip(),
            "Матчи": str(match_).strip(),
            "аншлаг": str(soldout).strip(),
            "Зрителей": str(audience).strip(),
            "В среднем": str(average).strip(),
            "Команда": name
        }
def main(links):
    df = DataFrame(
        columns=["Сезон", "Лига", "Матчи", "аншлаг", "Зрителей", "В среднем", "Команда"]
    )
    for link in links:
        try:
            parse(link, df)
            print(f"[+] Спарсили успешно `{link}`")
        except Exception as err:
            print(f"[-] Ошибка при парсинге `{link}`")
            print(str(err))
    return df
linkslaliga = [
        "https://www.transfermarkt.com/real-madrid/besucherzahlenentwicklung/verein/418",
        "https://www.transfermarkt.world/fc-barcelona/besucherzahlenentwicklung/verein/131",
        "https://www.transfermarkt.world/atletico-madrid/besucherzahlenentwicklung/verein/13",
        "https://www.transfermarkt.world/athletic-bilbao/besucherzahlenentwicklung/verein/621",
        "https://www.transfermarkt.world/fc-villarreal/besucherzahlenentwicklung/verein/1050",
        "https://www.transfermarkt.world/real-betis-sevilla/besucherzahlenentwicklung/verein/150",
        "https://www.transfermarkt.world/rayo-vallecano/besucherzahlenentwicklung/verein/367",
        "https://www.transfermarkt.world/celta-vigo/besucherzahlenentwicklung/verein/940",
        "https://www.transfermarkt.world/ca-osasuna/besucherzahlenentwicklung/verein/331",
        "https://www.transfermarkt.world/rcd-mallorca/besucherzahlenentwicklung/verein/237",
        "https://www.transfermarkt.world/real-sociedad-san-sebastian/besucherzahlenentwicklung/verein/681",
        "https://www.transfermarkt.world/fc-valencia/besucherzahlenentwicklung/verein/1049",
        "https://www.transfermarkt.world/fc-getafe/besucherzahlenentwicklung/verein/3709",
        "https://www.transfermarkt.world/deportivo-alaves/besucherzahlenentwicklung/verein/1108",
        "https://www.transfermarkt.world/fc-girona/besucherzahlenentwicklung/verein/12321",
        "https://www.transfermarkt.world/fc-sevilla/besucherzahlenentwicklung/verein/368",
        "https://www.transfermarkt.world/espanyol-barcelona/besucherzahlenentwicklung/verein/714",
        "https://www.transfermarkt.world/ud-levante/besucherzahlenentwicklung/verein/3368",
        "https://www.transfermarkt.world/fc-elche/besucherzahlenentwicklung/verein/1531",
        "https://www.transfermarkt.world/real-oviedo/besucherzahlenentwicklung/verein/2497",
    ]
linkspremier = [
        "https://www.transfermarkt.world/fc-arsenal/besucherzahlenentwicklung/verein/11",
        "https://www.transfermarkt.world/aston-villa/besucherzahlenentwicklung/verein/405",
        "https://www.transfermarkt.world/afc-bournemouth/besucherzahlenentwicklung/verein/989",
        "https://www.transfermarkt.world/fc-brentford/besucherzahlenentwicklung/verein/1148",
        "https://www.transfermarkt.world/brighton-amp-hove-albion/besucherzahlenentwicklung/verein/1237",
        "https://www.transfermarkt.world/fc-burnley/besucherzahlenentwicklung/verein/1132",
        "https://www.transfermarkt.world/fc-chelsea/besucherzahlenentwicklung/verein/631",
        "https://www.transfermarkt.world/crystal-palace/besucherzahlenentwicklung/verein/873",
        "https://www.transfermarkt.world/fc-everton/besucherzahlenentwicklung/verein/29",
        "https://www.transfermarkt.world/fc-fulham/besucherzahlenentwicklung/verein/931",
        "https://www.transfermarkt.world/leeds-united/besucherzahlenentwicklung/verein/399",
        "https://www.transfermarkt.world/fc-liverpool/besucherzahlenentwicklung/verein/31",
        "https://www.transfermarkt.world/manchester-city/besucherzahlenentwicklung/verein/281",
        "https://www.transfermarkt.world/manchester-united/besucherzahlenentwicklung/verein/985",
        "https://www.transfermarkt.world/newcastle-united/besucherzahlenentwicklung/verein/762",
        "https://www.transfermarkt.world/nottingham-forest/besucherzahlenentwicklung/verein/703",
        "https://www.transfermarkt.world/afc-sunderland/besucherzahlenentwicklung/verein/289",
        "https://www.transfermarkt.world/tottenham-hotspur/besucherzahlenentwicklung/verein/148",
        "https://www.transfermarkt.world/west-ham-united/besucherzahlenentwicklung/verein/379",
        "https://www.transfermarkt.world/wolverhampton-wanderers/besucherzahlenentwicklung/verein/543"
    ]
linksbun = [
        "https://www.transfermarkt.world/fc-bayern-munchen/besucherzahlenentwicklung/verein/27",
        "https://www.transfermarkt.world/bayer-04-leverkusen/besucherzahlenentwicklung/verein/15",
        "https://www.transfermarkt.world/eintracht-frankfurt/besucherzahlenentwicklung/verein/24",
        "https://www.transfermarkt.world/borussia-dortmund/besucherzahlenentwicklung/verein/16",
        "https://www.transfermarkt.world/sc-freiburg/besucherzahlenentwicklung/verein/60",
        "https://www.transfermarkt.world/1-fsv-mainz-05/besucherzahlenentwicklung/verein/39",
        "https://www.transfermarkt.world/rasenballsport-leipzig/besucherzahlenentwicklung/verein/23826",
        "https://www.transfermarkt.world/sv-werder-bremen/besucherzahlenentwicklung/verein/86",
        "https://www.transfermarkt.world/vfb-stuttgart/besucherzahlenentwicklung/verein/79",
        "https://www.transfermarkt.world/borussia-monchengladbach/besucherzahlenentwicklung/verein/18",
        "https://www.transfermarkt.world/vfl-wolfsburg/besucherzahlenentwicklung/verein/82",
        "https://www.transfermarkt.world/fc-augsburg/besucherzahlenentwicklung/verein/167",
        "https://www.transfermarkt.world/1-fc-union-berlin/besucherzahlenentwicklung/verein/89",
        "https://www.transfermarkt.world/fc-st-pauli/besucherzahlenentwicklung/verein/35",
        "https://www.transfermarkt.world/tsg-1899-hoffenheim/besucherzahlenentwicklung/verein/533",
        "https://www.transfermarkt.world/1-fc-heidenheim-1846/besucherzahlenentwicklung/verein/2036",
        "https://www.transfermarkt.world/1-fc-koln/besucherzahlenentwicklung/verein/3",
        "https://www.transfermarkt.world/hamburger-sv/besucherzahlenentwicklung/verein/41"
    ]
linksport = [
        "https://www.transfermarkt.world/sporting-lissabon/besucherzahlenentwicklung/verein/336",
        "https://www.transfermarkt.world/benfica-lissabon/besucherzahlenentwicklung/verein/294",
        "https://www.transfermarkt.world/fc-porto/besucherzahlenentwicklung/verein/720",
        "https://www.transfermarkt.world/sc-braga/besucherzahlenentwicklung/verein/1075",
        "https://www.transfermarkt.world/cd-santa-clara/besucherzahlenentwicklung/verein/2423",
        "https://www.transfermarkt.world/vitoria-guimaraes-sc/besucherzahlenentwicklung/verein/2420",
        "https://www.transfermarkt.world/fc-famalicao/besucherzahlenentwicklung/verein/3329",
        "https://www.transfermarkt.world/gd-estoril-praia/besucherzahlenentwicklung/verein/1465",
        "https://www.transfermarkt.world/casa-pia-ac/besucherzahlenentwicklung/verein/3268",
        "https://www.transfermarkt.world/moreirense-fc/besucherzahlenentwicklung/verein/979",
        "https://www.transfermarkt.world/rio-ave-fc/besucherzahlenentwicklung/verein/2425",
        "https://www.transfermarkt.world/fc-arouca/besucherzahlenentwicklung/verein/8024",
        "https://www.transfermarkt.world/gil-vicente-fc/besucherzahlenentwicklung/verein/2424",
        "https://www.transfermarkt.world/cd-nacional/besucherzahlenentwicklung/verein/982",
        "https://www.transfermarkt.world/cf-estrela-amadora-sad/besucherzahlenentwicklung/verein/2431",
        "https://www.transfermarkt.world/avs-futebol-sad/besucherzahlenentwicklung/verein/110302",
        "https://www.transfermarkt.world/cd-tondela/besucherzahlenentwicklung/verein/7179",
        "https://www.transfermarkt.world/fc-alverca/besucherzahlenentwicklung/verein/2521",
    ]
linksliga1 = [
        "https://www.transfermarkt.world/fc-paris-saint-germain/besucherzahlenentwicklung/verein/583",
        "https://www.transfermarkt.world/olympique-marseille/besucherzahlenentwicklung/verein/244",
        "https://www.transfermarkt.world/as-monaco/besucherzahlenentwicklung/verein/162",
        "https://www.transfermarkt.world/ogc-nizza/besucherzahlenentwicklung/verein/417",
        "https://www.transfermarkt.world/losc-lille/besucherzahlenentwicklung/verein/1082",
        "https://www.transfermarkt.world/olympique-lyon/besucherzahlenentwicklung/verein/1041",
        "https://www.transfermarkt.world/rc-strassburg-alsace/besucherzahlenentwicklung/verein/667",
        "https://www.transfermarkt.world/rc-lens/besucherzahlenentwicklung/verein/826",
        "https://www.transfermarkt.world/stade-brest-29/besucherzahlenentwicklung/verein/3911",
        "https://www.transfermarkt.world/fc-toulouse/besucherzahlenentwicklung/verein/415",
        "https://www.transfermarkt.world/aj-auxerre/besucherzahlenentwicklung/verein/290",
        "https://www.transfermarkt.world/fc-stade-rennes/besucherzahlenentwicklung/verein/273",
        "https://www.transfermarkt.world/fc-nantes/besucherzahlenentwicklung/verein/995",
        "https://www.transfermarkt.world/sco-angers/besucherzahlenentwicklung/verein/1420",
        "https://www.transfermarkt.world/ac-le-havre/besucherzahlenentwicklung/verein/738",
        "https://www.transfermarkt.world/fc-lorient/besucherzahlenentwicklung/verein/1158",
        "https://www.transfermarkt.world/paris-fc/besucherzahlenentwicklung/verein/10004",
        "https://www.transfermarkt.world/fc-metz/besucherzahlenentwicklung/verein/347"
    ]
linksseriaa = [
        "https://www.transfermarkt.world/ssc-neapel/besucherzahlenentwicklung/verein/6195",
        "https://www.transfermarkt.world/inter-mailand/besucherzahlenentwicklung/verein/46",
        "https://www.transfermarkt.world/atalanta-bergamo/besucherzahlenentwicklung/verein/800",
        "https://www.transfermarkt.world/juventus-turin/besucherzahlenentwicklung/verein/506",
        "https://www.transfermarkt.world/as-rom/besucherzahlenentwicklung/verein/12",
        "https://www.transfermarkt.world/ac-florenz/besucherzahlenentwicklung/verein/430",
        "https://www.transfermarkt.world/lazio-rom/besucherzahlenentwicklung/verein/398",
        "https://www.transfermarkt.world/ac-mailand/besucherzahlenentwicklung/verein/5",
        "https://www.transfermarkt.world/fc-bologna/besucherzahlenentwicklung/verein/1025",
        "https://www.transfermarkt.world/como-1907/besucherzahlenentwicklung/verein/1047",
        "https://www.transfermarkt.world/fc-turin/besucherzahlenentwicklung/verein/416",
        "https://www.transfermarkt.world/udinese-calcio/besucherzahlenentwicklung/verein/410",
        "https://www.transfermarkt.world/genua-cfc/besucherzahlenentwicklung/verein/252",
        "https://www.transfermarkt.world/hellas-verona/besucherzahlenentwicklung/verein/276",
        "https://www.transfermarkt.world/cagliari-calcio/besucherzahlenentwicklung/verein/1390",
        "https://www.transfermarkt.world/parma-calcio-1913/besucherzahlenentwicklung/verein/130",
        "https://www.transfermarkt.world/us-lecce/besucherzahlenentwicklung/verein/1005",
        "https://www.transfermarkt.world/us-sassuolo/besucherzahlenentwicklung/verein/6574",
        "https://www.transfermarkt.world/ac-pisa-1909/besucherzahlenentwicklung/verein/4172",
        "https://www.transfermarkt.world/us-cremonese/besucherzahlenentwicklung/verein/2239"
    ]


"""ла лига"""
laliga = main(linkslaliga)
laliga_selected = (
    laliga[laliga["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
laliga_selected["Лига"] = laliga_selected["Лига"].replace(
    {"ЛаЛига": "La Liga", "Лалига": "La Liga", "LaLiga": "La Liga"}
)
laliga_selected = laliga_selected[laliga_selected["Лига"] == "La Liga"]

"""премьер лига"""
premier = main(linkspremier)
premier = (
    premier[premier["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
premier["Лига"] = premier["Лига"].replace(
    {"Премьер-Лига": "Premier League"}
)
premier = premier[premier["Лига"] == "Premier League"]

"""бундеслига"""
bun = main(linksbun)
bun = (
    bun[bun["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
bun["Лига"] = bun["Лига"].replace({"Бундеслига": "Bundesliga"})
bun = bun[bun["Лига"] == "Bundesliga"]

"""португалия"""
port = main(linksport)
port = (
    port[port["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
port["Лига"] = port["Лига"].replace(
    {"Лига betclic": "Liga Portugal", "Лига NOS": "Liga Portugal"}
)
port = port[port["Лига"] == "Liga Portugal"]

"""лига1"""
liga1 = main(linksliga1)
liga1 = (
    liga1[liga1["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
liga1["Лига"] = liga1["Лига"].replace({"Лига 1": "Ligue 1"})
liga1 = liga1[liga1["Лига"] == "Ligue 1"]

"""серия а"""
seriaa = main(linksseriaa)
seriaa = (
    seriaa[seriaa["Сезон"].isin(["24/25", "23/24", "22/23", "21/22"])]
    .copy()
)
seriaa["Лига"] = seriaa["Лига"].replace({"Серия А": "Serie A"})
seriaa = seriaa[seriaa["Лига"] == "Serie A"]



all_attendance = pd.concat([laliga_selected, bun, premier, seriaa, liga1, port], ignore_index=True)
all_attendance["Команда"] = all_attendance["Команда"].str.replace("-", " ")
all_attendance["Сезон"] = all_attendance["Сезон"].apply(lambda x: f"20{x[:2]}-20{x[3:]}")

all_attendance.to_csv('attendance.csv', index=False, encoding='utf-8')