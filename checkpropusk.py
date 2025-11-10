from common import *


df = pd.read_csv("merged_years.csv")

print(len(df[df["year_of_foundation"] == "Nan"]))