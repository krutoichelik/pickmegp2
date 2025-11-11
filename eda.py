import matplotlib.pyplot as plt

import wikiapi
from common import *
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

df = pd.read_csv("squad_cost.csv")
df2 = pd.read_csv("matches_dataset.csv")

df["season"] = df["season"].apply(lambda x: x.replace("_", "-"))


merged = df2.merge(df, how="left", left_on=["team", "season"], right_on = ["team", "season"])

# print(merged.isna().sum()) # 1564 вышло 1564 из датасета в 16000+ строк

merged = merged.dropna()


# 1. Заводим вспомогательные колонки
merged["is_win"]  = (merged["result"] == "win")
merged["is_draw"] = (merged["result"] == "draw")
merged["is_loss"] = (merged["result"] == "lose")


stats = (
    merged
    .groupby(["league", "team", "season"], as_index=False)
    .agg(
        games=("result", "size"),
        wins=("is_win", "sum"),
        draws=("is_draw", "sum"),
        losses=("is_loss", "sum"),
        pts_total=("pts", "sum"),
    )
)
stats["avg_res_for_game"] = (stats["wins"] * 3 + stats["draws"] * 1) / stats["games"]

stats["year_of_foundation"] = stats["team"].progress_apply(wikiapi.get_wiki_html)
print(stats)

stats.to_csv("final_data.csv", index=False)
#
# data.to_csv("merged_years.csv", index=False)
# print(data)
