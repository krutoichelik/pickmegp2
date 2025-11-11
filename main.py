import matplotlib.pyplot as plt

from common import *


df = pd.read_csv("temp_final.csv")

plt.figure(figsize=(14, 14))
sns.heatmap(df.drop(columns=["league", "season", "team"]).corr(), annot=True, cmap="coolwarm")
plt.show()