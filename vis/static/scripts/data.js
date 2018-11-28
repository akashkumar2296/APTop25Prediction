var realMode = false; //set to true to use Python data.
var sim_aprankings = []
var simTimePoints = ['End of 1st', 'End of 2nd', 'End of 3rd', 'Final']
var simEquivalentTimeRem = ["2700", "1800", "900", "0"]
var currentSimTimePoint = 0;



function genSim_aprankings() {
	sim_aprankings = []
	for (var i=0; i<getCurrentWeek(); i++){
		sim_aprankings.push([])
	}
	for (var i=0; i<sim_team_details.length; i++) {
		week = parseInt(sim_team_details[i].week);
		rank = parseInt(sim_team_details[i].Rank);
		if (rank <= 25) {	
			sim_aprankings[week-1][rank-1] = sim_team_details[i].team
		}
	}
	for (var i=0; i<sim_team_details.length; i++) {
		week = parseInt(sim_team_details[i].week)-1;
		rank = parseInt(sim_team_details[i].PrevRank);
		if (week > 0 && rank <= 25 && sim_aprankings[week-1][rank-1] == undefined) {
			sim_aprankings[week-1][rank-1] = sim_team_details[i].team
		}
	}

}

function getCurrentWeek() 
{	
	if (realMode) {
		//TODO: retrieve the current week from Python
	}
	else 
		return parseInt(sim_in_progress_games[0].week);
}	


function getRankings(week) {
	if (realMode) {
		//TODO: retrieve AP rankings for the given week
		//returned data is an Array of 25 team names for the given week
		//week is an int from 1 to the last week number of the season.
	}
	else {
			if (sim_aprankings.length == 0) 
			genSim_aprankings();
		return sim_aprankings[week-1];
	}
}

function getPrediction() {
	prediction = []
	if (realMode) {
		//TODO: run ML model to get top 25 rankings prediction.
	}
	else {
		prediction = []
		for (var i=0; i<25; i++) {
			prediction.push("unknown");
		}
		prediction[1] = "Alabama";
		prediction[2] = "Clemson";
		prediction[3] = "NotreDame";
		prediction[4] = "Georgia";
		prediction[5] = "Michigan";
		prediction[8] = "LSU";
		prediction[7] = "OhioState";
		prediction[12] = "Kentucky";
		prediction[13] = "PennState";
		prediction[14] = "Florida";
		prediction[15] = "Syracuse";
		prediction[17] = "Pittsburgh";
		}
	return prediction;


}

function getUnknownPrediction() {
	prediction = []
	for (var i=0; i<25; i++) 
		prediction.push("unknown");
	return prediction;
}


function predictRanking(team) {
	if (realMode) {
		//TODO: run ML model to predict the ranking for the team
	}
	else {
		prediction = getPrediction();
		ranking = 50;
		for (var i=0; i<prediction.length; i++) {
			if (team == prediction[i]) {
				ranking = i+1;
				break;
			}
		}
		return ranking;

	}

}

function getTeamCurrentStats(team) {
	if (realMode) {
		//TODO: Retrieve current stats for team
	}
	else {
		teamStats = []
		for (var i=0; i<sim_in_progress_games.length; i++) {
			if (sim_in_progress_games[i].team == team && sim_in_progress_games[i].TimeRem == simEquivalentTimeRem[currentSimTimePoint]) {
				teamStats.push(sim_in_progress_games[i]);
				break;
			}
		}
		return teamStats;

	}
}

function getTeamStats(team, week) {
	if (realMode) {
		//TODO: Retrieve stats for team for week
	}
	else {
		teamStats = []
		for (var i=0; i<sim_team_details.length; i++) {
			if (sim_team_details[i].team == team && sim_team_details[i].week == week) {
				teamStats.push(sim_team_details[i]);
				break;
			}
		}
		return teamStats;

	}
}


function getGameData() {

	if (realMode) {
		//TODO: Retrieve game schedule for the week
		//returned an array of objects that contains the following attributes: 
		// {team1:{id:<string>, score:<int>}, team2:{id:<string>, score:<int>}, time:<string>}
		// team1 is the home team, team2 is the away team; if both teams are away, put the higher rank team is team1
		// id: the team name should match the list in data.js
		// score: in-game score or the final score for completed games
		// time: remaining game time; 0 for completed games

	}
	else {
		var scoredata=[]
		game_teams = []
		for (var i=0; i<sim_in_progress_games.length; i++) {
			if (sim_in_progress_games[i]["TimeRem"] != simEquivalentTimeRem[currentSimTimePoint])
				continue;
			team = sim_in_progress_games[i]["team"];
			if (game_teams.includes(team))
				continue;
			OppTeam = sim_in_progress_games[i]["OppTeam"]
			game_teams.push(team);
			game_teams.push(OppTeam);
			score = sim_in_progress_games[i]["ScoreDiff"]
			HAN = sim_in_progress_games[i]["HAN"]
			min = "0" + Math.floor(parseInt(sim_in_progress_games[i]["TimeRem"])/60).toString()
			min = min.substr(min.length-2,2);
			sec = "0" + Math.floor(parseInt(sim_in_progress_games[i]["TimeRem"])/3600).toString();
			sec = sec.substr(sec.length-2,2);
			timeRem = "Time: " + min + ":" + sec
			if (HAN == 'H') {
				team1 = team
				team2 = OppTeam
				if (score > 0) {
					score1 = score
					score2 = 0
				}
				else {
					score1 = 0
					score2 = -score
				}
			}
			else if (HAN=='A') {
				team2 = team
				team1 = OppTeam
				if (score > 0) {
					score2 = score
					score1 = 0
				}
				else {
					score2 = 0
					score1 = -score
				}
			}
			else {
				team1 = team
				team2 = OppTeam
				if (score > 0) {
					score1 = score
					score2 = 0
				}
				else {
					score1 = 0
					score2 = -score
				}
			}

			scoredata.push({team1: {id:team1, score:score1}, team2:{id:team2,score:score2} , time: timeRem});
		}
		return scoredata;
	}	
		
		
}

