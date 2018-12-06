//This script manages the drawing, refresh and tooltips on the AP ranking grid.

var rankingGridData = [];
var predictionShown = getUnknownPrediction();  //stores which of the 25 predictions are being displayed
var weekShowing;

//draw the week numbers header column
function drawWeekHeaders(grid, headerCells, tile_size, num_week) {
	var weekHeader = grid.selectAll(".weekheader")
		.data(headerCells)
		.enter()
		.append("text")
		.filter(function(d, i) {return i>0;})
		.attr("class","heading")
		.attr("x", function(d) { return d.x+tile_size.w/2-12; })
		.attr("y", function(d) { return d.y+tile_size.h/2+5; })
		.attr("font-size", "10px")
		.attr("fill", "red")
		.text(function(d, i) { 
					var week=i+getCurrentWeek()-num_week;
					if (week == getCurrentWeek()) return "PRE"; 
					else return "W"+ week;
				});
}


//draw the ranking # header row
function drawRankingHeaders(grid, rankingHeaderCells, tile_size) {
	var rankingHeader = grid.selectAll(".rankingheader")
		.data(rankingHeaderCells)
		.enter()
		.append("text")
		.filter(function(d, i) {return i>0;})
		.attr("class","heading")
		.attr("x", function(d) { return d.x+tile_size.w/2-12; })
		.attr("y", function(d) { return d.y+tile_size.h/2+5; })
		.attr("font-size", "10px")
		.attr("fill", "red")
		.text(function(d, i) { return "#"+(i+1)});

}

//build tooltips
//loop through all the attributes in the statistics object and display them
function tooltip_text(d) {
	var tooltips = "<strong>" + d.team + "</strong><br>" 
	var week = parseInt(d.week) + getCurrentWeek() - weekShowing - 1;
	if (week == getCurrentWeek())
		var teamStats = getTeamCurrentStats(d.team)
	else
		var teamStats = getTeamStats(d.team, (week).toString());
	if (teamStats.length == 0) {
		tooltips += "No information available."
	}
	else {
		teamStats = teamStats[0];
		for (x in teamStats) {
			if (x != "team")
				tooltips += x + ": " + teamStats[x] + "<br>" 
		}
	}
	return tooltips;
}

var tooltip = d3.tip()
	.attr('class', 'tooltip')
	.offset([150,80])
	.html(function(d) {return tooltip_text(d);});

//draw the rankings for a week
function drawRankings(grid, rankingCells, rankings, background, week) {
	grid.selectAll(".rankings")
		.data(rankingCells)
		.enter()
		.append("rect")
		.filter(function(d, i) {if (i==0) return false; else {d.team = rankings[i-1]; d.week = week; return true;}})
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width*0.9; })
		.attr("height", function(d) { return d.height*0.9; })
		.attr("fill", background)
		.on("mouseover", tooltip.show)
		.on("mouseout", tooltip.hide)
		;

	grid.selectAll(".rankings")
		.data(rankingCells)
		.enter()
		.append("svg:image")
	    .filter(function(d, i) {return i>0;})
		.attr("xlink:href",  function(d,i) {
			if (rankings[i] == undefined) 
				imgname = "nodata.png"
			else
			    imgname = rankings[i].toLowerCase() + ".png";
			return "static/images/" + imgname;})
		.attr("x", function(d) { return d.x+3; })
		.attr("y", function(d) { return d.y+2; })
		.attr("width", function(d) { return d.width*0.8; })
		.attr("height", function(d) { return d.height*0.8; })
		.on("mouseover", tooltip.show)
		.on("mouseout", tooltip.hide)
		;
}


//draw the predictions
function drawPredictionRow(grid) {
	drawRankings(grid, rankingGridData[weekShowing+1], predictionShown, predictcolor, weekShowing+1 );
}


//main driver to draw the complete AP Ranking Grid.
function showRankingsGrid(grid, num_week, tile_size) {
	rankingGridData = makeGridData(num_week+1, num_team, tile_size);
	var colBasedGridData = rowToColBasedGridData(rankingGridData)
	drawWeekHeaders(grid, colBasedGridData[0], tile_size, num_week);
	drawRankingHeaders(grid, rankingGridData[0], tile_size);
	for (var i=1; i<=num_week; i++) {
		drawRankings(grid, rankingGridData[i], getRankings(i+getCurrentWeek()-num_week-1), apcolor, i);
	}
	drawPredictionRow(grid);

	grid.call(tooltip);
}
