
var num_week = 16;
var num_team = 25;
var rankings_tile_size = {w:35, h:25}
var score_tile_size = {w:60, h:60}
// var svg_size = {w:rankings_tile_size.w*(num_team)+100, h:rankings_tile_size.h*(num_week)+100}
var apcolor = "lightgray";
var predictcolor = "cyan";

function calSvgSize(row, col, tile_size) {
	return {w:tile_size.w*col+50, h:tile_size.h*row+50}
}


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


function drawGrid(gridData) {

	var row = grid.selectAll(".row")
		.data(gridData)
		.enter().append("g")
		.attr("class", "row");
	
	var column = row.selectAll(".square")
		.data(function(d) { return d; })
		.enter().append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", "#fff")
		// .style("stroke", "#222")
		// .on('click', function(d) {
		// d.click ++;
		// if ((d.click)%4 == 0 ) { d3.select(this).style("fill","#fff"); }
		// if ((d.click)%4 == 1 ) { d3.select(this).style("fill","#2C93E8"); }
		// if ((d.click)%4 == 2 ) { d3.select(this).style("fill","#F56C4E"); }
		// if ((d.click)%4 == 3 ) { d3.select(this).style("fill","#838690"); }
		// })
		;

	column.forEach(function(e) { e.style("fill", "lightgray")});
}

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


function drawWeekHeaders(grid, headerCells, tile_size) {
	var weekHeader = grid.selectAll(".weekheader")
		.data(headerCells)
		.enter()
		.append("text")
		.filter(function(d, i) {return i>0;})
		.attr("class","colheader")
		.attr("x", function(d) { return d.x+tile_size.w/2-12; })
		.attr("y", function(d) { return d.y+tile_size.h/2+5; })
		.attr("font-size", "10px")
		.attr("fill", "red")
		.text(function(d, i) { return "WK"+ (i+1);});
}


function drawRankingHeaders(grid, rankingHeaderCells, tile_size) {
	var rankingHeader = grid.selectAll(".rankingheader")
		.data(rankingHeaderCells)
		.enter()
		.append("text")
		.filter(function(d, i) {return i>0;})
		.attr("class","rowheader")
		.attr("x", function(d) { return d.x+tile_size.w/2-12; })
		.attr("y", function(d) { return d.y+tile_size.h/2+5; })
		.attr("font-size", "10px")
		.attr("fill", "red")
		.text(function(d, i) { return "#"+(i+1);});

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

function showTooltip(week, team) {

}

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



function showRankingsGrid(grid, num_week) {
	var gridData = makeGridData(num_week, num_team, rankings_tile_size);
	var colBasedGridData = rowToColBasedGridData(gridData)
	drawWeekHeaders(grid, colBasedGridData[0], rankings_tile_size);
	drawRankingHeaders(grid, gridData[0], rankings_tile_size);
	for (var i=1; i<num_week; i++) {
		drawRankings(grid, gridData[i], getRankings(i), apcolor, i);
	}
	drawRankings(grid, gridData[num_week], getRankings(num_week), predictcolor, num_week );
}

function showScoreGrid(grid, num_week) {
	var gridData = makeGridData(num_week, num_team, score_tile_size);
	var colBasedGridData = rowToColBasedGridData(gridData)
	for (var i=1; i<num_week; i++) {
		drawRankings(grid, gridData[i], getRankings(i), apcolor, i);
	}
	drawRankings(grid, gridData[num_week], getRankings(num_week), predictcolor, num_week );
}

var rGridSize = calSvgSize(5,27,rankings_tile_size);


var rankings_grid = d3.select("#grid")
	.append("svg")
	.attr("width",rGridSize.w+"px")
	.attr("height",rGridSize.h+"px");


rankings_grid.call(tooltip);
// showRankingsGrid(rankings_grid, 5);

var radius = 25;
var circles = d3.range(5).map(function() {
	return {
	  x: Math.round(Math.random() * (rGridSize.w - radius * 2) + radius),
	  y: Math.round(Math.random() * (rGridSize.h - radius * 2) + radius)
	};
  });

  var color = d3.scale.ordinal()
	  .range(d3.schemeCategory20);
  
var gamedata1 = {
	 id: "gamedata1"
	,team1: {id:"georgia", score: 24}
	,team2: {id:"alabama", score: 0}
	,time: {q:"3rd",r:"4:34"}
}
var gamedata2 = {
	id: "gamedata2"
   ,team1: {id:"lsu", score: 24}
   ,team2: {id:"miss", score: 0}
   ,time: {q:"4th",r:"0:50"}
}

var boxdata1 = { x: 50, y: 50, width:100, height:100};
var boxdata2 = { x: 80, y: 100, width:80, height:80};



function drawScorebox(svgarea, gamedata, boxdata) {

	svgdata = new Array();
	svgdata.push(gamedata);

	var scorebox = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("rect")
	.attr("x", boxdata.x)
	.attr("y",boxdata.y)
	.attr("width", boxdata.width)
	.attr("height", boxdata.height)
	.style("fill", "lightgray")
	.style("stroke", "#222");

	var team1 = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("svg:image")
	.attr("xlink:href",  function(d) { return "/static/images/" + d.team1.id +".png"})
	.attr("x", boxdata.x+2)
	.attr("y", boxdata.y)
	.attr("width", boxdata.width/3)
	.attr("height", boxdata.height/3)
	.style("stroke", "black");

	var score1 = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("text")
	.attr("x", boxdata.x+2)
	.attr("y", boxdata.y+boxdata.height/3+15)
	.text(function(d) {return d.team1.score})
	.classed("score", true);


	var team2 = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("svg:image")
	.attr("xlink:href",  function(d) { return "/static/images/" + d.team2.id +".png"})
	.attr("x", boxdata.x+boxdata.width*2/3-2)
	.attr("y", boxdata.y)
	.attr("width", boxdata.width/3)
	.attr("height", boxdata.height/3)
	.style("stroke", "black");

	var score2 = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("text")
	.attr("x", boxdata.x+boxdata.width-18)
	.attr("y", boxdata.y+boxdata.height/3+15)
	.text(function(d) {return d.team2.score})
	.classed("score", true);

	var timeq = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("text")
	.attr("x", boxdata.x+2)
	.attr("y", boxdata.y+boxdata.height/3*2+10)
	.text(function(d) {return d.time.q})
	.classed("time", true);

	var timer = svgarea.selectAll(".scorebox")
	.data(svgdata)
	.enter()
	.append("text")
	.attr("x", boxdata.x+25)
	.attr("y", boxdata.y+boxdata.height/3*2+10)
	.text(function(d) {return d.time.r})
	.classed("time", true);


	return {box:scorebox, team1:team1, team2:team2, score1:score1, score2:score2, timeq:timeq, timer:timer};

}

function updateScorebox(svgarea, gamedata, boxdata, scorebox) {
	// scorebox.box.remove();

	// box:scorebox, team1:team1, team2:team2, score1:score1, score2:score2, timeq:timeq, timer:timer
	// for (var k in scorebox) {
	// 	k.remove();
	// }

	drawScorebox(svgarea, gamedata, boxdata);
}


var scorebox1 = drawScorebox(rankings_grid, gamedata1, boxdata1);
// scorebox1 = updateScorebox(rankings_grid, gamedata2, boxdata1, scorebox1); 



// rankings_grid.selectAll(".scorebubble")
// 	.data(circles)
// 	.enter().append("rect")
// 	  .attr("x", function(d) { return d.x; })
// 	  .attr("y", function(d) { return d.y; })
// 	  .attr("width", function(d) { return radius*2 })
// 	  .attr("height", function(d) { return radius*2 })
// 	  .style("fill", "blue")
// 		.style("stroke", "#222")
// 		.call(d3.drag()
// 		  .on("start", dragstarted)
// 		  .on("drag", dragged)
// 		  .on("end", dragended))
// 	  .on("dblclick", dblclick);


//   rankings_grid.selectAll(".scorebubble")
// 	  .data(circles)
// 	  .enter()
// 	  .append("svg:image")
// 	  .attr("xlink:href",  "/static/images/georgia.png")
// 	  .attr("x", function(d) { return d.x; })
// 	  .attr("y", function(d) { return d.y; })
// 	  .attr("width", function(d) { return radius })
// 	  .attr("height", function(d) { return radius});



	  
  
  function dragstarted(d) {
	d3.select(this).raise().classed("active", true);
  }
  function dblclick(d) {
	d3.select(this).attr("width", d3.select(this).attr("width") * 1.2 > radius * 2 ? radius : d3.select(this).attr("width") * 1.2 );
	d3.select(this).attr("height", d3.select(this).attr("height") * 1.2 > radius * 2 ? radius : d3.select(this).attr("height") * 1.2 );
  }
  
  function dragged(d) {
	d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
  }
  
  function dragended(d) {
	d3.select(this).classed("active", false);
  }
  

// var sGridSize = calSvgSize(13,13,score_tile_size);
// var score_grid = d3.select("#grid")
// 	.append("svg")
// 	.attr("width",sGridSize.w+"px")
// 	.attr("height",sGridSize.h+"px");
// showScoreGrid(score_grid, 12);
