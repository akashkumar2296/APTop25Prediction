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


