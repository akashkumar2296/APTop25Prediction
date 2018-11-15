var cachedPrediction = new Array();
var realMode = false; //set to true to use Python data.

function getCurrentWeek() 
{	
	if (realMode) {
		//TODO: retrieve the current week from Python
	}
	else 
		return sim_currentweek;
}	

function getRankings(week) {
	if (realMode) {
		//TODO: retrieve AP rankings for the given week
		//returned data is an Array of 25 team names for the given week
		//week is an int from 1 to the last week number of the season.
	}
	else {
		return sim_aprankings[week-1]
	}
}

function getPrediction() {
	if (cachedPrediction.length == 0)
		cachedPrediction = retrievePrediction();
	
	return cachedPrediction;
}


function predictRanking(teamstats) {
	if (realMode) {
		//TODO: run ML model to predict the ranking for the team and return the rankings for the 2 teams in an object {team1:<int>, team2:<int>}
		//teamstats is an object with the following attributes:
		//{team:<string>, HAN:<string>, oppteam:<string>, scoreDiff:<int>, winLose:<string>, 
		// OT:<boolean>, toDiff:<int>, yppDiff:<decimal>, PenYdDiff:<int>, topDiff:<int>, winPer:<decimal>}
		//NOTE: some of the features, such as PreRank, RankDiff, etc. should be available in Python
	}
	else {
		var rank1 = Math.floor(Math.random()*25)+1;
		var rank2 = Math.floor(Math.random()*25)+1;
		return {team1:rank1, team2:rank2} 
	}

}

function retrievePrediction() {
	if (realMode) {
		//TODO: retrieve current top 25 predictions
		//return an Array of 25 team names
		//if the prediction is not available yet, return an empty array.
	}
	else {
		var rankings = getRankings(getCurrentWeek());
		var prediction = new Array();
		console.log(prediction);
		for (var i=0; i < rankings.length; i++)
			prediction.push(rankings[i]);
		team0 = prediction[0]
		team5 = prediction[5]
		team13 = prediction[13]
		team24 = prediction[24]
		prediction[0] = team5;
		prediction[5] = team0;
		prediction[13] = team24;
		prediction[24] = team13;
		return prediction;
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
		return sim_scoredata;
	}	
		
		
}

