import pandas as pd
import html5lib
import lxml.html
import requests
import time
from datetime import datetime
base_url = "https://frc-events.firstinspires.org"
year = datetime.now().year
teams = {}

for year in range(2006,year+1):
    url = base_url + "/" + str(year)
    r = requests.get(url)
    dom = lxml.html.fromstring(r.content)
    for link in dom.xpath('//a/@href'):
        comp = str(link)
        print(comp)
        if len(comp) > 5 and len(comp) <17:
            awards_url = base_url + comp + "/" +"awards"
            r2 = requests.get(awards_url)
            winners = pd.read_html(r2.content)[0]
            for rows in range(len(winners)):
                awards = str(winners.xs(rows).take([0])).split()
                if 'Winner' in awards:
                    team = str(winners.xs(rows).take([1])).split()[2]
                    if team in teams:
                        teams[team][0] += 1
                    else:
                        teams[team] = [1,0,0]
                elif 'Chairmans' in awards or "Chairman's" in awards:
                    team = str(winners.xs(rows).take([1])).split()[2]
                    if team in teams:
                        teams[team][1] += 1
                    else:
                        teams[team] = [0,1,0]
                elif 'Engineering' in awards and 'Inspiration' in awards:
                    team = str(winners.xs(rows).take([1])).split()[2]
                    if team in teams:
                        teams[team][2] += 1
                    else:
                        teams[team] = [0,0,1]

team_nums = []
wins = []
chairman = []
EI = []
for key in teams:
    if key != "NaN":
        team_nums.append(int(key))
        wins.append(teams[key][0])
        chairman.append(teams[key][1])
        EI.append(teams[key][2])

frc = pd.DataFrame({"Team":team_nums, "Wins":wins, "Chairmans":chairman, "E.I.":EI})
frc.sort_values("Team", inplace=True)
writer = pd.ExcelWriter("FRC_Teams.xlsx", engine="xlsxwriter")
frc.to_excel(writer, sheet_name="Team stats", columns=["Team", "Wins", "Chairmans", "E.I."], startcol=0, startrow=0, index=False)
writer.save()
