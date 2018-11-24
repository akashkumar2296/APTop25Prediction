import csv

header = ['Year', 'team', 'week', 'PrevRank', 'RankDiff', 'Conference', 'HAN', 'FavUnd', 'OppTeam', 'OppConf', 'ScoreDiff', 'WinLose', 'OT', 'TODiff', 'YPPDiff', 'PenYdDiff', 'TOPDiff', 'GameStatus', 'WinPer', 'TimeRem', 'Rank']
teams  = []

with open("../../../model/Dataset_Final_Historical_data.csv", newline="") as csvfile:
    hisdata = list(csv.reader(csvfile))
with open("../../../model/Dataset_Final_Completed_Game_Data.csv", newline="") as csvfile:
    cpdata = list(csv.reader(csvfile))
with open("../../../model/Dataset_Final_InProgress_Game_Data.csv", newline="") as csvfile:
    ipdata = list(csv.reader(csvfile))


with open("../scripts/sim_team_details.js", "w") as jsFile:
    jsFile.write("var sim_team_details = new Array();\n")
    for i in range(1, len(hisdata)):
        if (hisdata[i][0] == "2018"):
            line = "    sim_team_details.push({"
            for j in range(len(header)-1):
                line += header[j+1] + ":"
                line += '"' + hisdata[i][j+1].strip().replace(" ","") + '",'
                if (header[j+1] == "team" and hisdata[i][j+1].strip().replace(" ","") not in teams):
                    teams.append(hisdata[i][j+1].strip().replace(" ",""))
            line = line[:len(line)-1] +"});\n"
            jsFile.write(line)
    for i in range(1, len(cpdata)):
        if (cpdata[i][0] == "2018"):
            line = "    sim_team_details.push({"
            for j in range(len(header)-1):
                line += header[j+1] + ":"
                line += '"' + cpdata[i][j+1].strip().replace(" ","") + '",'
                if (header[j+1] == "team" and cpdata[i][j+1].strip().replace(" ","") not in teams):
                    teams.append(cpdata[i][j+1].strip().replace(" ",""))
            line = line[:len(line)-1] +"});\n"
            jsFile.write(line)

team_pairs = []
with open("../scripts/sim_in_progress_games.js", "w") as jsFile:
    jsFile.write("var sim_in_progress_games = new Array();\n")
    for i in range(1, len(ipdata)):
        if (ipdata[i][0] == "2018"):
            if ([ipdata[i][1], ipdata[i][8]] in team_pairs or [ipdata[i][8], ipdata[i][1]] in team_pairs):
                continue
            team_pairs.append([ipdata[i][1], ipdata[i][8]])
            team_pair1 = [ipdata[i][1], ipdata[i][8]]
            line = "    sim_in_progress_games.push({"
            for j in range(len(header)-1):
                line += header[j+1] + ":"
                line += '"' + ipdata[i][j+1].strip().replace(" ","") + '",'
                if (header[j+1] == "team" and ipdata[i][j+1].strip().replace(" ","") not in teams):
                    teams.append(ipdata[i][j+1].strip().replace(" ",""))
            line = line[:len(line)-1] +"});\n"
            jsFile.write(line)

with open("../scripts/teams.js", "w") as jsFile:
    jsFile.write("var teams = new Array();\n")
    for i in range(len(teams)):
        line = '    teams.push({id:"' + teams[i].strip().replace(" ","") +'", display:"' + teams[i].strip() +'"});\n'
        jsFile.write(line)

