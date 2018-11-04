var num_week = 16;
var num_team = 25;
var tile_size = {w:35, h:25}
var svg_size = {w:tile_size.w*(num_team)+100, h:tile_size.h*(num_week)+100}
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
var apcolor = "lightgray";
var predictcolor = "cyan";


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

function getPrediction(week) {
	var rankings=new Array();
	for (i=0; i<25; i++) {
 		rankings.push(teams[Math.floor(Math.random() * teams.length)]);
	}
	return rankings;
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


function drawWeekHeaders(headerCells, gridData) {
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


function drawRankingHeaders(rankingHeaderCells, gridData) {
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

function drawRankings(rankingCells, rankings, background, week) {

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




var grid = d3.select("#grid")
	.append("svg")
	.attr("width",svg_size.w+"px")
	.attr("height",svg_size.h+"px");




grid.call(tooltip);
	


var gridData = makeGridData(num_week, num_team, tile_size);
var colBasedGridData = rowToColBasedGridData(gridData)
// drawGrid(gridData);
drawWeekHeaders(colBasedGridData[0]);
drawRankingHeaders(gridData[0]);
drawRankings(gridData[1], getPrediction(1), apcolor, 1 );
drawRankings(gridData[2], getPrediction(2), apcolor, 2);
drawRankings(gridData[3], getPrediction(3), apcolor, 3);
drawRankings(gridData[4], getPrediction(4), predictcolor, 4);
