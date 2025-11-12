from common import *

merged = pd.read_csv("final_data.csv")

df3 = pd.read_csv("attendance.csv")
df3 = df3.drop(columns="Матчи")

df3 = df3.rename(columns={
    "Сезон": "season",
    "Лига": "league",
    "Матчи": "matches",
    "аншлаг": "sellouts",
    "Зрителей": "total_attendance",
    "В среднем": "avg_attendance",
    "Команда": "team",
})

df3["total_attendance"] = df3["total_attendance"].apply(lambda x : x.replace(",", ""))
df3["total_attendance"] = df3["total_attendance"].apply(lambda x : x.replace(".", ""))
df3["avg_attendance"] = df3["avg_attendance"].apply(lambda x : x.replace(",", ""))
df3["avg_attendance"] = df3["avg_attendance"].apply(lambda x : x.replace(".", ""))


teams_map = {
    'real madrid': 'Real Madrid CF',
    'fc barcelona': 'FC Barcelona',
    'atletico madrid': 'Club Atlético de Madrid',
    'athletic bilbao': 'Athletic Club',
    'fc villarreal': 'Villarreal CF',
    'real betis sevilla': 'Real Betis Balompié',
    'rayo vallecano': 'Rayo Vallecano de Madrid',
    'celta vigo': 'RC Celta de Vigo',
    'ca osasuna': 'CA Osasuna',
    'rcd mallorca': 'RCD Mallorca',
    'real sociedad san sebastian': 'Real Sociedad de Fútbol',
    'fc valencia': 'Valencia CF',
    'fc getafe': 'Getafe CF',
    'deportivo alaves': 'Deportivo Alavés',
    'fc girona': 'Girona FC',
    'fc sevilla': 'Sevilla FC',
    'espanyol barcelona': 'RCD Espanyol de Barcelona',
    'ud levante': 'Levante UD',
    'fc elche': 'Elche CF',

    'fc bayern munchen': 'FC Bayern München',
    'bayer 04 leverkusen': 'Bayer 04 Leverkusen',
    'eintracht frankfurt': 'Eintracht Frankfurt',
    'borussia dortmund': 'BV Borussia 09 Dortmund',
    'sc freiburg': 'SC Freiburg',
    '1 fsv mainz 05': '1. FSV Mainz 05',
    'rasenballsport leipzig': 'RB Leipzig',
    'sv werder bremen': 'SV Werder Bremen',
    'vfb stuttgart': 'VfB Stuttgart',
    'borussia monchengladbach': 'Borussia Mönchengladbach',
    'vfl wolfsburg': 'VfL Wolfsburg',
    'fc augsburg': 'FC Augsburg',
    '1 fc union berlin': '1. FC Union Berlin',
    'tsg 1899 hoffenheim': 'TSG 1899 Hoffenheim',
    '1 fc heidenheim 1846': '1. FC Heidenheim 1846',
    '1 fc koln': '1. FC Köln',

    'fc arsenal': 'Arsenal FC',
    'aston villa': 'Aston Villa FC',
    'afc bournemouth': 'AFC Bournemouth',
    'fc brentford': 'Brentford FC',
    'brighton amp hove albion': 'Brighton & Hove Albion FC',
    'fc burnley': 'Burnley FC',
    'fc chelsea': 'Chelsea FC',
    'crystal palace': 'Crystal Palace FC',
    'fc everton': 'Everton FC',
    'fc fulham': 'Fulham FC',
    'leeds united': 'Leeds United FC',
    'fc liverpool': 'Liverpool FC',
    'manchester city': 'Manchester City FC',
    'manchester united': 'Manchester United FC',
    'newcastle united': 'Newcastle United FC',
    'nottingham forest': 'Nottingham Forest FC',
    'tottenham hotspur': 'Tottenham Hotspur FC',
    'west ham united': 'West Ham United FC',
    'wolverhampton wanderers': 'Wolverhampton Wanderers FC',

    'ssc neapel': 'SSC Napoli',
    'inter mailand': 'FC Internazionale Milano',
    'atalanta bergamo': 'Atalanta BC',
    'juventus turin': 'Juventus FC',
    'as rom': 'AS Roma',
    'ac florenz': 'ACF Fiorentina',
    'lazio rom': 'SS Lazio',
    'ac mailand': 'AC Milan',
    'fc bologna': 'Bologna FC 1909',
    'fc turin': 'Torino FC',
    'udinese calcio': 'Udinese Calcio',
    'genua cfc': 'Genoa CFC',
    'hellas verona': 'Hellas Verona FC',
    'cagliari calcio': 'Cagliari Calcio',
    'us lecce': 'US Lecce',
    'us sassuolo': 'US Sassuolo Calcio',

    'fc paris saint germain': 'Paris Saint-Germain FC',
    'olympique marseille': 'Olympique de Marseille',
    'as monaco': 'AS Monaco FC',
    'ogc nizza': 'OGC Nice',
    'losc lille': 'Lille OSC',
    'olympique lyon': 'Olympique Lyonnais',
    'rc strassburg alsace': 'RC Strasbourg Alsace',
    'rc lens': 'RC Lens',
    'stade brest 29': 'Stade Brestois 29',
    'fc toulouse': 'Toulouse FC',
    'fc stade rennes': 'Stade Rennais FC',
    'fc nantes': 'FC Nantes',
    'sco angers': 'Angers SCO',
    'ac le havre': 'Le Havre AC',
    'fc lorient': 'FC Lorient',
    'fc metz': 'FC Metz',

    'sporting lissabon': 'Sporting CP',
    'benfica lissabon': 'Sport Lisboa e Benfica',
    'fc porto': 'FC Porto',
    'sc braga': 'SC Braga',
    'cd santa clara': 'CD Santa Clara',
    'vitoria guimaraes sc': 'Vitória SC',
    'fc famalicao': 'FC Famalicão',
    'gd estoril praia': 'Estoril Praia',
    'casa pia ac': 'Casa Pia AC',
    'moreirense fc': 'Moreirense FC',
    'rio ave fc': 'Rio Ave FC',
    'fc arouca': 'FC Arouca',
    'gil vicente fc': 'Gil Vicente FC',
    'cf estrela amadora sad': 'CF Estrela da Amadora',
    'cd tondela': 'CD Tondela',
}

df3["team"] = df3["team"].str.lower().map(teams_map)
df3 = df3.drop(columns="league")
df4 = merged.merge(df3, how="left", left_on=["season", "team"], right_on=["season", "team"])
df4.to_csv("temp_final.csv", index=False)
print(df4)