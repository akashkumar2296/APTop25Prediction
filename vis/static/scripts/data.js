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
	// var gamedata1 = {
	//    team1: {id:"georgia", score: 24}
	//    ,team2: {id:"alabama", score: 0}
	//    ,time: "3rd - 4:34"
	// }
	// var gamedata2 = {
	//   team1: {id:"lsu", score: 45}
	//   ,team2: {id:"westernmi", score: 23}
	//   ,time: "4th - 0:50"
	// }

	// var gamedata3 = {
	// 	id: "gamedata3"
	//    ,team1: {id:"houston", score: 45}
	//    ,team2: {id:"kentucky", score: 23}
	//    ,time: "1st - 2:34"
	//  }
 
	var boxdata1 = { width:80, height:80};
	
	scoreboxdata = new Array();
	// scoreboxdata.push({g:gamedata1, b:boxdata1});
	// scoreboxdata.push({g:gamedata2, b:boxdata1});
	// scoreboxdata.push({g:gamedata3, b:boxdata1});

	scoreboxdata.push({g:{team1: {id:"ballstate", score:0 }, team2:{id:"westernmi",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"ohio", score:0 }, team2:{id:"buffalo",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"northernil", score:0 }, team2:{id:"miamioh",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"coloradost", score:0 }, team2:{id:"utahst",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"oklahomast", score:0 }, team2:{id:"westvirginia",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"rutgers", score:0 }, team2:{id:"pennstate",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"alabama", score:0 }, team2:{id:"citadel",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"texas", score:0 }, team2:{id:"iowast",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"florida", score:0 }, team2:{id:"idaho",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"ucf", score:0 }, team2:{id:"cincinnati",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"lsu", score:0 }, team2:{id:"rice",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"maryland", score:0 }, team2:{id:"ohiostate",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"washingtonst", score:0 }, team2:{id:"arizona",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"washington", score:0 }, team2:{id:"oregonst",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"oklahoma", score:0 }, team2:{id:"kansas",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"georgia", score:0 }, team2:{id:"umass",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"clemson", score:0 }, team2:{id:"duke",score:0} , time: "1st - 5:00"}, b:boxdata1});
	scoreboxdata.push({g:{team1: {id:"syracuse", score:0 }, team2:{id:"notredame",score:0} , time: "1st - 5:00"}, b:boxdata1});
	
	
	
	return scoreboxdata;
}

