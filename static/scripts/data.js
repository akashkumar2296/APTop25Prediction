//This is the interface between the UI and back-end services.  
//All REST service calls and data generation are done in this script.


var realMode = false; //set to true to use Python data.
var sim_aprankings = []
var simTimePoints = ['End of 1st', 'End of 2nd', 'End of 3rd', 'Final']
var simEquivalentTimeRem = ["2700", "1800", "900", "0"]
var currentSimTimePoint = 0;



//determine the AP rankings from sim_team_details either based on the Rank or PrevRank attributes
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

//returns the current week
function getCurrentWeek() 
{	
	if (realMode) {
		//TODO: retrieve the current week from Python
	}
	else 
		return parseInt(sim_in_progress_games[0].week);
}	


//returns the AP rankings for the week
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

//returns the prediction for all teams at the end of the quarter
//the callback function is provided by the caller to process the data returned by the REST
function getPrediction(callback, quarter) {
	if(quarter){

		$.ajax({  
		// you may modify the URL to point to localhost as follows or modify the URL to point to your hosting server
		// url: 'http://localhost:5001/prediction/All'+'/'+quarter,  
		   url: 'http://www.ap25predictor.com/prediction/All'+'/'+quarter,  
		   type: 'GET',  
		   dataType: 'json',  
		   crossDomain: true,
		   success: function (data, textStatus, xhr) {  
			console.log("predicted ranking of  is ",data, " in quarter ", quarter);  // ***** Data = Team's Ranking ******
			callback(data, quarter)
		   },  
		   error: function (xhr, textStatus, errorThrown) {  
			console.log('Error in Operation', textStatus, errorThrown);  
			callback(undefined, quarter)
		   }  
		});
	}
	else{
		$.ajax({  
		// you may modify the URL to point to localhost as follows or modify the URL to point to your hosting server
		// url: 'http://localhost:5001/prediction/All',  
		   url: 'http://www.ap25predictor.com/prediction/All',  
		   type: 'GET',  
		   dataType: 'json',  
		   crossDomain: true,
		   success: function (data, textStatus, xhr) {  
			console.log("predicted ranking of is ",data);  // ***** Data = Team's Ranking ******
			callback(data, 4)
		   },  
		   error: function (xhr, textStatus, errorThrown) {  
			console.log('Error in Operation');  
			callback(undefined, 4)
		   }  
		});

	}

}

//generate a list of prediction placeholders
function getUnknownPrediction() {
	prediction = []
	for (var i=0; i<25; i++) 
		prediction.push("unknown");
	return prediction;
}


//call the REST to predict ranking of team for quarter
//callback from the caller to process the data returned by the REST
function predictRanking(callback, team, quarter=null) {

	var team_name;
	for (var i=0; i<teams.length; i++) {
		if (teams[i].id == team) {
			team_name = teams[i].display;
			break;
		}
	}

	if(quarter){

		$.ajax({  
		// you may modify the URL to point to localhost as follows or modify the URL to point to your hosting server
		// url: 'http://localhost:5001/prediction/'+team_name+'/'+quarter,  
		url: 'http://www.ap25predictor.com/prediction/'+team_name+'/'+quarter,  
		type: 'GET',  
		   dataType: 'json',  
		   crossDomain: true,
		   success: function (data, textStatus, xhr) {  
			console.log("predicted ranking of ", team_name, " is ",data, " in quarter ", quarter);  // ***** Data = Team's Ranking ******
			callback(team, data)
		   },  
		   error: function (xhr, textStatus, errorThrown) {  
			console.log('Error in Operation', textStatus, errorThrown);  
			callback(team, undefined)
		   }  
		});
	}
	else{
		$.ajax({  
		// you may modify the URL to point to localhost as follows or modify the URL to point to your hosting server
		// url: 'http://localhost:5001/prediction/'+team_name,  
		   url: 'http://www.ap25predictor.com/prediction/'+team_name,  
		   type: 'GET',  
		   dataType: 'json',  
		   crossDomain: true,
		   success: function (data, textStatus, xhr) {  
			console.log("predicted ranking of ", team_name, " is ",data);  // ***** Data = Team's Ranking ******
			callback(team, data)
		   },  
		   error: function (xhr, textStatus, errorThrown) {  
			console.log('Error in Operation');  
			callback(team, undefined)
		   }  
		});

	}

}

//return the team statistics from sim_in_progress_games
//this is used to simulate real-time data feed
function getTeamCurrentStats(team, quarter=null) {
		teamStats = []
		for (var i=0; i<sim_in_progress_games.length; i++) {
			if (sim_in_progress_games[i].team == team && sim_in_progress_games[i].TimeRem == simEquivalentTimeRem[currentSimTimePoint]) {
				teamStats.push(sim_in_progress_games[i]);
				break;
			}
		}
		return teamStats;
}


//return historical team statistics from sim_team_details
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



//return real-time game data from sim_in_progress_games
//this is used to simulate real-time data feed
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

