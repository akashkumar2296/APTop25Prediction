var deltaX = 0;
var deltaY = 0;

function dragstarted_scorebox(d) {
	d3.select(this).raise().classed("active", true);
  }

function dragged_scorebox(d) {

	d3.select(this).selectAll("rect.scorebox")
    .attr("x", d3.event.x - d.offsetx)
	.attr("y", d3.event.y - d.offsety) ;

	d3.select(this).selectAll("rect.scorebox")
    .attr("x", d3.event.x - d.offsetx)
	.attr("y", d3.event.y - d.offsety) ;


	d3.select(this).selectAll("text.score.team1")
    .attr("x", d3.event.x - d.offsetx + d.score1offsetx)
    .attr("y", d3.event.y - d.offsety + d.score1offsety);

	d3.select(this).selectAll("text.score.team2")
    .attr("x", d3.event.x - d.offsetx + d.score2offsetx)
    .attr("y", d3.event.y - d.offsety + d.score2offsety);

	d3.select(this).selectAll("text.time")
    .attr("x", d3.event.x - d.offsetx + d.timeoffsetx)
    .attr("y", d3.event.y - d.offsety + d.timeoffsety);

	
	d3.select(this).selectAll("image.team1")
    .attr("x", d3.event.x+d.image1offsetx - d.offsetx)
	.attr("y", d3.event.y+d.image1offsety - d.offsety);

	d3.select(this).selectAll("image.team2")
    .attr("x", d3.event.x+d.image2offsetx - d.offsetx)
	.attr("y", d3.event.y+d.image2offsety- d.offsety);

}
  
function dragended_scorebox(d) {
	d3.select(this).classed("active", false);
  }

//build tooltips
function tooltip_text_team(team) {
	var tooltips = "<strong>" + team + "</strong><br>" 
	var teamStats = getTeamStats(team);
	if (teamStats.length == 0) {
		tooltips += "No information available."
	}
	else {
		// sim_in_progress_games.push({team:"AirForce",week:"1",PrevRank:"50",RankDiff:"0",Conference:"MWC",HAN:"H",FavUnd:"F",OppTeam:"StonyBrook",OppConf:"FCS",ScoreDiff:"38",WinLose:"Win",OT:"N",TODiff:"",YPPDiff:"",PenYdDiff:"",TOPDiff:"",GameStatus:"Completed",WinPer:"100.000",TimeRem:"0",Rank:"50"});

		teamStats = teamStats[0];
		for (x in teamStats) {
			if (x != "team" && x != "week")
				tooltips += x + ": " + teamStats[x] + "<br>" 
		}
	}
	return tooltips;
}

function tooltip_team1_text(d) {
	return tooltip_text_team(d.team1.id);
}

var tooltip_team1 = d3.tip()
	.attr('class', 'tooltip')
	.offset([80,80])
	.html(function(d) {return tooltip_team1_text(d);});

function tooltip_team2_text(d) {	
	return tooltip_text_team(d.team2.id);
}

var tooltip_team2 = d3.tip()
	.attr('class', 'tooltip')
	.offset([80,80])
	.html(function(d) {return tooltip_team2_text(d);});


function drawScorebox3(svgarea, scoreboxdata, tile_size) {
	var width = parseInt(svgarea.style("width"), 10);
	var height = parseInt(svgarea.style("height"), 10);
	var num_col = Math.floor(width / tile_size.w);

	var scorebox = svgarea.selectAll("*")
    .data(scoreboxdata)
	.enter().append("g")	
    .attr("transform", function(d, i) { 
		var colnum = i % num_col;
		var rownum = Math.floor(i / num_col);
		d.offsetx = colnum*tile_size.w;
		d.offsety = rownum*tile_size.h;
		return "translate(" + d.offsetx + "," + d.offsety + ")"; })
	// .call(d3.drag()
  	// 		.on("start", dragstarted_scorebox)
	// 		.on("drag", dragged_scorebox)
	// 		.on("end", dragended_scorebox))
			;



	scorebox.append("rect")
	.attr("x", 1)
	.attr("y", 1)
	.attr("width", function(d) {return tile_size.w*0.95})
	.attr("height", function(d) {return tile_size.h*0.95})
	.style("fill", "lightgray")
	.style("stroke", "#222")
	.classed("scorebox", true)
	;


	scorebox.append("image")
	.attr("xlink:href",  function(d) { d.team=1; return "static/images/" + d.team1.id +".png"})
	.attr("team", 2)
	.attr("x", function(d) { d.image1offsetx = 2; return d.image1offsetx;})
	.attr("y", function(d) { d.image1offsety = 2; return d.image1offsety;})
	.attr("width", function(d) {return tile_size.w/3})
	.attr("height", function(d) {return tile_size.h/3})
	.classed("team1", true)
	.on("mouseover", tooltip_team1.show)
	.on("mouseout", tooltip_team1.hide)
	.on("dblclick", function(d,i) {
		if (d.predicted == undefined || !d.predicted) {
			d.predicted = true;
			predict = predictRanking(d.team1.id);
			if (predict > 25) {
				alert(d.team1.id + " is Ranked " + predict);
			}
			else {
				predictionShown[predict-1] = d.team1.id;
				drawPredictionRow(rankings_grid);
			}
		}
		else {
			d.predicted = false;
			for (var i=0; i<predictionShown.length; i++) {
				if (predictionShown[i] == d.team1.id) {
					predictionShown[i] = "unknown";
					drawPredictionRow(rankings_grid);
					break;
				}
			}
		}
	})
	.style("stroke", "black");

	scorebox.append("image")
	.attr("xlink:href",  function(d) { d.team=2; return "static/images/" + d.team2.id +".png"})
	.attr("team", 2)
	.attr("x", function(d) { d.image2offsetx = tile_size.w - 30; return d.image2offsetx;}) 
	.attr("y", function(d) { d.image2offsety = 2; return d.image2offsety;})
	.attr("width", function(d) {return tile_size.w/3})
	.attr("height", function(d) {return tile_size.h/3})
	.classed("team2", true)
	.on("mouseover", tooltip_team2.show)
	.on("mouseout", tooltip_team2.hide)
	.on("dblclick", function(d,i) {
		if (d.predicted == undefined || !d.predicted) {
			d.predicted = true;
			predict = predictRanking(d.team2.id);
			if (predict > 25) {
				alert(d.team2.id + " is Ranked " + predict);
			}
			else {
				predictionShown[predict-1] = d.team2.id;
				drawPredictionRow(rankings_grid);
			}
		}
		else {
			d.predicted = false;
			for (var i=0; i<predictionShown.length; i++) {
				if (predictionShown[i] == d.team2.id) {
					predictionShown[i] = "unknown";
					drawPredictionRow(rankings_grid);
					break;
				}
			}
		}
	})
	.style("stroke", "black");

	scorebox.append("text")
	.attr("x", function(d) { d.score1offsetx = 2; return d.score1offsetx; })
	.attr("y", function(d) { d.score1offsety = 45; return d.score1offsety;})
	.text(function(d) {return d.team1.score})
	.on("mouseover", tooltip_team1.show)
	.on("mouseout", tooltip_team1.hide)
	.classed("score", true)
	.classed("team1", true);

	scorebox.append("text")
	.attr("x", function(d) { d.score2offsetx = tile_size.w-20; return d.score2offsetx; })
	.attr("y", function(d) { d.score2offsety = 45; return d.score2offsety;})
	.text(function(d) {return d.team2.score})
	.on("mouseover", tooltip_team2.show)
	.on("mouseout", tooltip_team2.hide)
	.classed("score", true)
	.classed("team2", true);

	scorebox.append("text")
	.attr("x", function(d) { d.timeoffsetx = 2; return d.timeoffsetx; })
	.attr("y", function(d) { d.timeoffsety = 65; return d.timeoffsety;})
	.text(function(d) {return d.time})
	.classed("time", true);

	svgarea.call(tooltip_team1);
	svgarea.call(tooltip_team2);
	return scorebox;
}


function refreshScore(svgarea) {
	svgarea.selectAll("text.score.team1").text(function(d) { d.g.team1.score += 1; return d.g.team1.score;});
}


