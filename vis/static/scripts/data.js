var teams =["alabama",
			"bc",
			"clemson",
			"fl",
			"fresno",
			"georgia",
			"houston",
			"iowa",
			"lsu",
			"mi",
			"miss",
			"notre",
			"ohiostate",
			"ok",
			"pennstate",
			"syracuse",
			"tam",
			"texas",
			"ucf",
			"uk",
			"utah",
			"utahstate",
			"virginia",
			"ws",
			"wv"]

function getCurrentWeek() {
	return 12;
}	

function getRankings(week) {
	var rankings=new Array();
	for (i=0; i<25; i++) {
		var newTeam = teams[Math.floor(Math.random() * teams.length)];
		var found = false;
		for (j=0; j<rankings.length && !found; j++) {
			found = rankings[j] == newTeam;
		}
		if (found) 
			i--;
		else
	 		rankings.push(newTeam);
	}
	return rankings;
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
	  ,team2: {id:"miss", score: 23}
	  ,time: "4th - 0:50"
	}

	var gamedata3 = {
		id: "gamedata3"
	   ,team1: {id:"houston", score: 45}
	   ,team2: {id:"uk", score: 23}
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

