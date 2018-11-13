
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
					var week=i+2+getCurrentWeek()-num_week;
					if (week > getCurrentWeek()) return "PRE"; 
					else return "W"+ week;
				});
}


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
function tooltip_text(d) {
	var tooltips = "<strong>Team " + d.team + " in Week "+ d.week + "</strong><br>";
	tooltips += "Show some stats here......<br>";
	tooltips += "or some charts, etc.<br>";
	return tooltips;
}

var tooltip = d3.tip()
	.attr('class', 'tooltip')
	.offset([80,80])
	.html(function(d) {return tooltip_text(d);});

function drawRankings(grid, rankingCells, rankings, background, week) {

	grid.selectAll(".rankings")
		.data(rankingCells)
		.enter()
		.append("rect")
		.filter(function(d, i) {d.team = rankings[i]; d.week = week; return i>0;})
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
		.filter(function(d, i) {d.team = rankings[i]; d.week = week; return i>0;})
		.attr("xlink:href",  function(d,i) { return "/static/images/" + rankings[i] + ".png";})
		.attr("x", function(d) { return d.x+3; })
		.attr("y", function(d) { return d.y+2; })
		.attr("width", function(d) { return d.width*0.8; })
		.attr("height", function(d) { return d.height*0.8; })
		.on("mouseover", tooltip.show)
		.on("mouseout", tooltip.hide)
		;
}



function showRankingsGrid(grid, num_week, tile_size) {
	var gridData = makeGridData(num_week+1, num_team, tile_size);
	var colBasedGridData = rowToColBasedGridData(gridData)
	drawWeekHeaders(grid, colBasedGridData[0], tile_size, num_week+1);
	drawRankingHeaders(grid, gridData[0], tile_size);
	for (var i=1; i<=num_week; i++) {
		drawRankings(grid, gridData[i], getRankings(i+getCurrentWeek()-num_week), apcolor, i);
	}
	drawRankings(grid, gridData[num_week+1], getPrediction(), predictcolor, num_week+1 );
	grid.call(tooltip);
}
