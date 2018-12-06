//The main driver script for the UI.
//It uses d3 to build the 4 SVG on the index.html temaplate:
//#gridcontrol contains the button controls and drop-down for prediction and week filtering functions
//#grid contains the AP ranking grid
//#scoreboard contains the game tiles
//#simulation contains the button controls and labels on the bottom for simulation functions.


//parameters that drive the grid and tile sizes
var num_week = 16;
var num_team = 25;
var rankings_tile_size = {w:35, h:35}
var score_tile_size = {w:80, h:80}
var apcolor = "lightgray";
var predictcolor = "cyan";

//determine the size of SVG needed based on the grid and tile sizes
function calSvgSize(row, col, tile_size) {
	return {w:tile_size.w*col+50, h:tile_size.h*row+50}
}

//build a 2-dim array to model each cell in the AP ranking grid to facilitate d3 calls
//this approach is too restrictive and was not used at the end
function makeGridData(rowcount, colcount, tile_size) {
	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
	var ypos = 1;
	var width = tile_size.w;
	var height = tile_size.h;
	var click = 0;
	
	// iterate for rows	
	for (var row = 0; row < rowcount+1; row++) {
		data.push( new Array() );
		
		// iterate for cells/columns inside rows
		for (var column = 0; column < colcount+1; column++) {
			data[row].push({
				rownum: row,
				colnum: column,
				x: xpos,
				y: ypos,
				width: width,
				height: height,
				click: click,
			})
			// increment the x position. I.e. move it over by 50 (width variable)
			xpos += width;
		}
		// reset the x position after a row is complete
		xpos = 1;
		// increment the y position for the next row. Move it down 50 (height variable)
		ypos += height;	
	}
	return data;
}

//relate to using makeGridData for drawing a grid in d3
//not used in the final app
function rowToColBasedGridData(rowBasedData) {
	var colBasedData = new Array();
	rowBasedData[0].forEach(row => {
		colBasedData.push(new Array());
	})

	rowBasedData.forEach(row => {
		row.forEach(cell => {
			colBasedData[cell.colnum].push(cell);
		})
	});

	return colBasedData;
}


//******************************  #gridcontrol: build the control row on the top of UI

//week to show dropdown for filtering
var data = d3.range(1, getCurrentWeek());

var select = d3.select('#gridcontrol')
.append('text')
	.classed("option", true)
	.text('Weeks to show: ');

function onchange_weeksToShowOption() {
	weekShowing = parseInt(d3.select('select').property('value'));
	refreshRankingsGrid(weekShowing);
};
	
var select = d3.select('#gridcontrol')
.append('select')
	.classed("option", true)
	.on('change',onchange_weeksToShowOption)
	

var weeksToShowOptions = select
.selectAll('option')
	.data(d3.range(1, getCurrentWeek())).enter()
	.append('option')
		.classed("option", true)
		.text(function (d) { return d; });



d3.select('#gridcontrol')
.append('text')
.classed("option", true)
.text("  Current Week: " + getCurrentWeek() + " ");


function clearPrediction() {
	weekShowing = parseInt(d3.select('select').property('value'));
	predictionShown = getUnknownPrediction();
	drawPredictionRow(rankings_grid);	
}


// Cleare the prediction row
d3.select('#gridcontrol')
.append("button")
.text("Clear Prediction row")
.on("click", function(){ clearPrediction()})


// Run prediction and refresh the prediction row
d3.select('#gridcontrol')
.append("button")
.text("Click to Predict: ")
.on("click", function(){ showPrediction() })

//callback to display returned predicted ranking of a team
function showPredictionHandle(team, ranking) {
	if (ranking == undefined) {
		predictMsg.text(team + ": Predicted Ranking is unavailable");
	}
	else {
		predictMsg.text(team + ": Predicted Ranking #" + ranking);
	}
}

//callback to display returned predicted rankings of top 25
function showAllPredictionsHandle(rankings, quarter) {
	if (rankings == undefined) {
		predictMsg.text("Top 25 Predictions not yet available");
	}
	else {
		predictMsg.text("Top 25 Predictions shown at end of Quarter " + quarter);
		clearPrediction();
		for (var i=0; i< rankings.length; i++) {
			if (rankings[i].ranking <= 25) {
				predictionShown[rankings[i].ranking-1] = rankings[i].team.replace(" ","");
			}
		}
		drawPredictionRow(rankings_grid);
	}
}


//call the data interface to run predictions
function showPrediction() {
	var team = selectTeam.property('value');
	weekShowing = parseInt(d3.select('select').property('value'));

	if (team == "Top 25") {
		getPrediction(showAllPredictionsHandle, currentSimTimePoint+1);
	}
	else {
		predictRanking(showPredictionHandle, team, currentSimTimePoint+1);
	}
}

//Team prediction selection
var select = d3.select('#gridcontrol')
.append('text')
	.classed("option", true)
	.text(' >>');

function onchange_teamPredictOption(d) {
	team = d3.select(this).property('value');
};
	
var selectTeam = d3.select('#gridcontrol')
.append('select')
	.classed("option", true)
	.on('change',onchange_teamPredictOption);

var predictOption = teams.slice(0);
predictOption.unshift({id:"Top 25"});

var teamPredictOption = selectTeam
.selectAll('option')
	.data(predictOption).enter()
	.append('option')
		.text(function (d) { return d.id; });

var predictMsg = d3.select('#gridcontrol')
.append('text')
.classed("option", true)
.text("");



//******************************  #grid: build the AP Ranking grid

function refreshRankingsGrid(num_weeks) {
	var num_weeks = parseInt(num_weeks);
	var rGridSize = calSvgSize(num_weeks+1,27,rankings_tile_size);
	d3.select("#grid").selectAll("*").remove();
	rankings_grid = d3.select("#grid")
		.append("svg")
		.attr("width",rGridSize.w+"px")
		.attr("height",rGridSize.h+"px")
		;
	showRankingsGrid(rankings_grid, num_weeks, rankings_tile_size);
}


//******************************  #scoreboard: build the game tiles

function refreshScoreBoxes() {
	d3.select("#scoreboard").selectAll("*").remove();
	score_grid = d3.select("#scoreboard")
	.append("svg")
	.attr("width",sGridSize.w+"px")
	.attr("height",sGridSize.h+"px")
	;
	drawScorebox3(score_grid, getGameData(), score_tile_size);
}


var rGridSize = calSvgSize(5,27,rankings_tile_size);

var rankings_grid = d3.select("#grid")
	.append("svg")
	.attr("width",rGridSize.w+"px")
	.attr("height",rGridSize.h+"px")
	;


var sGridSize = calSvgSize(2,8,score_tile_size);

var score_grid = d3.select("#scoreboard")
	.append("svg")
	.attr("width",sGridSize.w+"px")
	.attr("height",sGridSize.h+"px")
	;

var scoreboxes = drawScorebox3(score_grid, getGameData(), score_tile_size);
weekShowing = parseInt(weeksToShowOptions.property('value'));
refreshRankingsGrid(weekShowing);



//******************************  #simulation: build the simulation controls

simulation_text = d3.select('#simulation')
.append("text")
.text("Current simulated time: " + simTimePoints[currentSimTimePoint] + "  ")
.classed("heading", true);

d3.select('#simulation').append("br")
d3.select('#simulation')
.append("text")
.text("Real-time data feed simulation is now:   ")
.classed("heading", true);

simulation_startstop = d3.select('#simulation')
	.append("button")
	.text("ON")
	.on("click", function() {
			if (simulating) {
				clearInterval(interval)
				d3.select(this).text("OFF")
			}
			else {
				interval = setInterval(function() { simulate_real_data() }, 2000);
				d3.select(this).text("ON")
			}
			simulating = !simulating;

		});


function advance_time() {
	currentSimTimePoint =(currentSimTimePoint + 1) % simTimePoints.length;
	simulation_text.text("Current simulated time: " + simTimePoints[currentSimTimePoint]+"  ");
	refreshScoreBoxes();
}
		
d3.select('#simulation').append("br")
d3.select('#simulation')
.append("text")
.text("Move to next quarter manually:   ")
.classed("heading", true);


simulation_move = d3.select('#simulation')
.append("button")
.text("Next")
.on("click", function() {
	currentSimTimePoint =(currentSimTimePoint + 1) % simTimePoints.length;
	simulation_text.text("Current simulated time: " + simTimePoints[currentSimTimePoint]+"  ");
	refreshScoreBoxes();
});


function simulate_real_data() {
	advance_time()
	getPrediction(showAllPredictionsHandle, currentSimTimePoint+1);
}

//refresh the simulation game data every 2 secs.
var interval = setInterval(function() { simulate_real_data() }, 2000);
var simulating = true;
