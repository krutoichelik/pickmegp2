import wikiapi
from common import *
import pandas as pd
from tqdm import tqdm

tqdm.pandas()  # включаем интеграцию с pandas

data = pd.read_csv("merged.csv")

data["year_of_foundation"] = data["team"].progress_apply(wikiapi.get_wiki_html)

data.to_csv("merged_years.csv", index=False)
print(data)