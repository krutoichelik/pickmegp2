import matplotlib.pyplot as plt

from common import *


df = pd.read_csv("temp_final.csv")

# plt.figure(figsize=(10, 10))
# sns.heatmap(df.drop(columns=["league", "season", "team"]).corr(), annot=True, cmap="coolwarm")
# plt.show()

plt.figure(figsize=(10, 10))
sns.histplot(data=df, x="total_cost", y="avg_res_for_game")
plt.show()