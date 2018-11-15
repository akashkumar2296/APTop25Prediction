var sim_currentweek = 12;

var sim_scoredata = new Array();
	sim_scoredata.push({team1: {id:"ballstate", score:0 }, team2:{id:"westernmi",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"ohio", score:0 }, team2:{id:"buffalo",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"northernil", score:0 }, team2:{id:"miamioh",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"coloradost", score:0 }, team2:{id:"utahst",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"oklahomast", score:0 }, team2:{id:"westvirginia",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"rutgers", score:0 }, team2:{id:"pennstate",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"alabama", score:0 }, team2:{id:"citadel",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"texas", score:0 }, team2:{id:"iowast",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"florida", score:0 }, team2:{id:"idaho",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"ucf", score:0 }, team2:{id:"cincinnati",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"lsu", score:0 }, team2:{id:"rice",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"maryland", score:0 }, team2:{id:"ohiostate",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"washingtonst", score:0 }, team2:{id:"arizona",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"washington", score:0 }, team2:{id:"oregonst",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"oklahoma", score:0 }, team2:{id:"kansas",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"georgia", score:0 }, team2:{id:"umass",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"clemson", score:0 }, team2:{id:"duke",score:0} , time: "60:00"});
	sim_scoredata.push({team1: {id:"syracuse", score:0 }, team2:{id:"notredame",score:0} , time: "60:00"});

var sim_aprankings = new Array();
    wkfake =["washingtonst","clemson","notredame","michigan","georgia","oklahoma","westvirginia","ohiostate","lsu","alabama","ucf","kentucky","syracuse","utahst","texas","fresnostate","bostoncollege","msstate","florida","washington","pennstate","ncstate","iowast","msstate","cincinnati"]
    wk11 =["alabama","clemson","notredame","michigan","georgia","oklahoma","westvirginia","ohiostate","lsu","washingtonst","ucf","kentucky","syracuse","utahst","texas","fresnostate","bostoncollege","msstate","florida","washington","pennstate","ncstate","iowast","msstate","cincinnati"]
    wk12 = ["alabama","clemson","notredame","michigan","georgia","oklahoma","westvirginia","washingtonst","ohiostate","lsu","ucf","syracuse","texas","utahst","florida","pennstate","washington","iowast","cincinnati","kentucky","utah","bostoncollege","boisestate","northwestern","msstate"]

for (var i=1; i <= sim_currentweek; i++) {
	var thisweek;
	try {
		thisweek = eval("wk"+i);
	} catch (error) {
		thisweek = wkfake;
	}
	sim_aprankings.push(thisweek); 
}


