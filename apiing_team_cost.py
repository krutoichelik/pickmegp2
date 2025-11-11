import requests
import pandas as pd

BASE_URL = "http://field-hub.online/api"
API_KEY = "fh_f2027e22b95edc2ecc26811849cd0195"

h = {"Authorization": f"Bearer {API_KEY}", "X-API-Key": API_KEY, "Accept": "application/json"}

r = requests.get(f"{BASE_URL}/manifest", headers=h, params={"_": "python"})

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


    payload = r.json()
    for i in payload["rows"]:
        i["season"] = ss
        df.loc[len(df)] = i


print(df)
df.to_csv("squad_cost.csv", index=False, encoding="utf-8")
