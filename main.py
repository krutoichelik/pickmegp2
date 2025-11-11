import matplotlib.pyplot as plt

from common import *


df = pd.read_csv("final_data.csv")

plt.figure(figsize=(16, 20))
sns.heatmap(df.drop(columns=["league", "season", "team"]).corr(), annot=True, cmap="coolwarm")
plt.show()