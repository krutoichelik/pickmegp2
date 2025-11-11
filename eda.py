import matplotlib.pyplot as plt

import wikiapi
from common import *
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

df = pd.read_csv("squad_cost.csv")
df2 = pd.read_csv("matches_dataset.csv")

df["season"] = df["season"].apply(lambda x: x.replace("_", "-"))


df2["is_win"] = (df2["result"] == "win")
df2["is_draw"] = (df2["result"] == "draw")
df2["is_loss"] = (df2["result"] == "lose")


stats = (
    df2
    .groupby(["league", "team", "season"], as_index=False)
    .agg(
        games=("result", "size"),
        wins=("is_win", "sum"),
        draws=("is_draw", "sum"),
        losses=("is_loss", "sum"),
        goals_total=("pts", "sum"),
    )
)

merged = stats.merge(df, how="left", left_on=["team", "season"], right_on=["team", "season"])
merged = merged.dropna()

merged["avg_res_for_game"] = (merged["wins"] * 3 + merged["draws"] * 1) / merged["games"]

merged["year_of_foundation"] = merged["team"].progress_apply(wikiapi.get_wiki_html)
print(merged)
merged.to_csv("final_data.csv", index=False)
#
# data.to_csv("merged_years.csv", index=False)
# print(data)


# БЕГЕМОТИКИ
