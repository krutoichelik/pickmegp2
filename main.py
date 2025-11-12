from common import *


df = pd.read_csv("final_data.csv")
df.rename(columns={"year_of_foundation": "club_age"}, inplace=True)

plt.figure(figsize=(10, 10))
sns.heatmap(df.drop(columns=["league", "season", "team"]).corr(), annot=True, cmap="coolwarm")
plt.show()

plt.figure(figsize=(10, 10))
sns.scatterplot(data=df, x="total_cost", y="avg_res_for_game", hue=df["avg_attendance"], palette="coolwarm")
plt.ylabel("Среднее количество очков за игру")
plt.xlabel("Стоимость состава")

plt.show()



plt.figure(figsize=(10, 10))
sns.scatterplot(data=df, hue="avg_res_for_game", y="avg_attendance", x=df["club_age"], palette="coolwarm")
plt.ylabel("Средняя посещаемость")
plt.xlabel("Возраст клуба")


plt.show()
