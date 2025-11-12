import requests
import pandas as pd
import logging
from logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

BASE_URL = "http://field-hub.online/api"
API_KEY = "fh_f2027e22b95edc2ecc26811849cd0195"

h = {"Authorization": f"Bearer {API_KEY}", "X-API-Key": API_KEY, "Accept": "application/json"}

r = requests.get(f"{BASE_URL}/manifest", headers=h, params={"_": "python"})
if r.status_code != 200:
    logger.error("manifest вернул статус %s", r.status_code)
else:
    logger.info("manifest успешно получен")   
    
mf = pd.DataFrame(r.json().get("datasets", []))

df = pd.DataFrame(columns=[
    "team", "players_amount", "avg_age",
    "foreign_players_amount", "team_cost_dif", "total_cost", "season"
])

parts = []

for i, row in mf.iterrows():
    lg = row["league"]
    ss = row["season"]

    r = requests.get(
        f"{BASE_URL}/data/{lg}/{ss}", headers=h, params={"format": "json", "api_key": API_KEY, "_": "python"})
    if r.status_code != 200:
        logger.error("ошибка запроса данных для лиги %s, сезона %s: статус %s", lg, ss, r.status_code)
        continue

    payload = r.json()
    for i in payload["rows"]:
        i["season"] = ss
        df.loc[len(df)] = i


print(df)
logger.info("сформирован DataFrame squad_cost, shape=%s", df.shape)
df.to_csv("squad_cost.csv", index=False, encoding="utf-8")
logger.info("Файл squad_cost.csv сохранён")      
