var currentPrediction = new Array();
var realMode = false;

function getCurrentWeek() 
{	
	if (realMode) {
		//TODO: plug in interface with Python model
	}
	else 
		return 12;
}	

function getRankings(week) {
	return aprankings[week-1]
}

function getPrediction() {
	if (currentPrediction.length == 0)
		currentPrediction = runPrediction();
	
	return currentPrediction;
}

function runPrediction() {
	if (realMode) {
		//TODO: plug in interface with Python model
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
	var gamedata1 = {
		id: "gamedata1"
	   ,team1: {id:"georgia", score: 24}
	   ,team2: {id:"alabama", score: 0}
	   ,time: "3rd - 4:34"
	}
	var gamedata2 = {
	   id: "gamedata2"
	  ,team1: {id:"lsu", score: 45}
	  ,team2: {id:"westernmi", score: 23}
	  ,time: "4th - 0:50"
	}

	var gamedata3 = {
		id: "gamedata3"
	   ,team1: {id:"houston", score: 45}
	   ,team2: {id:"kentucky", score: 23}
	   ,time: "1st - 2:34"
	 }
 
	var boxdata1 = { width:80, height:80};
	var boxdata2 = { width:40, height:40};
	
	scoreboxdata = new Array();
	scoreboxdata.push({g:gamedata1, b:boxdata1});
	scoreboxdata.push({g:gamedata2, b:boxdata1});
	scoreboxdata.push({g:gamedata3, b:boxdata1});
	
	return scoreboxdata;
}

