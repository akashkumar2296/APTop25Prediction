# This script is used to generate static data used on the UI
# The input CSV file names are hard-coded and must be updated whenever CSV data files are added or renamed
# It should not be run without review and update to see if the expected csv files still exists or not
import csv

header = ['Year', 'team', 'week', 'PrevRank', 'RankDiff', 'Conference', 'HAN', 'FavUnd', 'OppTeam', 'OppConf', 'ScoreDiff', 'WinLose', 'OT', 'TODiff', 'YPPDiff', 'PenYdDiff', 'TOPDiff', 'GameStatus', 'WinPer', 'TimeRem', 'Rank']
teams  = []

with open("../../../model/Dataset_Final_Historical_data.csv", newline="") as csvfile:
    hisdata = list(csv.reader(csvfile))
with open("../../../model/Dataset_Final_Completed_Game_Data_Weeks_9_Through_11.csv", newline="") as csvfile:
    cpdata = list(csv.reader(csvfile))
with open("../../../model/Dataset_Final_InProgress_Game_Data_Week_13.csv", newline="") as csvfile:
    ipdata = list(csv.reader(csvfile))
with open("../../../model/Dataset_Final_InProgress_Game_Data_Week_12.csv", newline="") as csvfile:
    wk12cpdata = list(csv.reader(csvfile))


#combining the historical data and the completed game data to generate the full set of team history up to the previous week
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
    for i in range(1, len(wk12cpdata)):
        if (wk12cpdata[i][0] == "2018"):
            line = "    sim_team_details.push({"
            for j in range(len(header)-1):
                line += header[j+1] + ":"
                line += '"' + wk12cpdata[i][j+1].strip().replace(" ","") + '",'
                if (header[j+1] == "team" and wk12cpdata[i][j+1].strip().replace(" ","") not in teams):
                    teams.append(wk12cpdata[i][j+1].strip().replace(" ",""))
            line = line[:len(line)-1] +"});\n"
            jsFile.write(line)

# Week #12 rank #9 - should be LSU - this need to added manually.

# data for the in-progress games.  This is used to simulate real-time data feeds
with open("../scripts/sim_in_progress_games.js", "w") as jsFile:
    jsFile.write("var sim_in_progress_games = new Array();\n")
    for i in range(1, len(ipdata)):
        if (ipdata[i][0] == "2018"):
            line = "    sim_in_progress_games.push({"
            for j in range(len(header)-1):
                line += header[j+1] + ":"
                line += '"' + ipdata[i][j+1].strip().replace(" ","") + '",'
                if (header[j+1] == "team" and ipdata[i][j+1].strip().replace(" ","") not in teams):
                    teams.append(ipdata[i][j+1].strip().replace(" ",""))
            line = line[:len(line)-1] +"});\n"
            jsFile.write(line)


# generate the list of teams as found in the datasets
with open("../scripts/teams.js", "w") as jsFile:
    jsFile.write("var teams = new Array();\n")
    for i in range(len(teams)):
        line = '    teams.push({id:"' + teams[i].strip().replace(" ","") +'", display:"' + teams[i].strip() +'"});\n'
        jsFile.write(line)

