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
		d.offsetx = colnum*d.b.width;
		d.offsety = rownum*d.b.height;
		return "translate(" + d.offsetx + "," + d.offsety + ")"; })
	.call(d3.drag()
  			.on("start", dragstarted_scorebox)
			.on("drag", dragged_scorebox)
			.on("end", dragended_scorebox))
			;

	scorebox.append("rect")
	.attr("x", 1)
	.attr("y", 1)
	.attr("width", function(d) {return d.b.width*0.95})
	.attr("height", function(d) {return d.b.height*0.95})
	.style("fill", "lightgray")
	.style("stroke", "#222")
	.classed("scorebox", true);

	scorebox.append("image")
	.attr("xlink:href",  function(d) { d.team=1; return "/static/images/" + d.g.team1.id +".png"})
	.attr("team", 2)
	.attr("x", function(d) { d.image1offsetx = 2; return d.image1offsetx;})
	.attr("y", function(d) { d.image1offsety = 2; return d.image1offsety;})
	.attr("width", function(d) {return d.b.width/3})
	.attr("height", function(d) {return d.b.height/3})
	.classed("team1", true)
	.style("stroke", "black");

	scorebox.append("image")
	.attr("xlink:href",  function(d) { d.team=2; return "/static/images/" + d.g.team2.id +".png"})
	.attr("team", 2)
	.attr("x", function(d) { d.image2offsetx = tile_size.w - 30; return d.image2offsetx;}) 
	.attr("y", function(d) { d.image2offsety = 2; return d.image2offsety;})
	.attr("width", function(d) {return d.b.width/3})
	.attr("height", function(d) {return d.b.height/3})
	.classed("team2", true)
	.style("stroke", "black");

	scorebox.append("text")
	.attr("x", function(d) { d.score1offsetx = 2; return d.score1offsetx; })
	.attr("y", function(d) { d.score1offsety = 45; return d.score1offsety;})
	.text(function(d) {return d.g.team1.score})
	.classed("score", true)
	.classed("team1", true);

	scorebox.append("text")
	.attr("x", function(d) { d.score2offsetx = d.b.width-20; return d.score2offsetx; })
	.attr("y", function(d) { d.score2offsety = 45; return d.score2offsety;})
	.text(function(d) {return d.g.team2.score})
	.classed("score", true)
	.classed("team2", true);

	scorebox.append("text")
	.attr("x", function(d) { d.timeoffsetx = 2; return d.timeoffsetx; })
	.attr("y", function(d) { d.timeoffsety = 65; return d.timeoffsety;})
	.text(function(d) {return d.g.time})
	.classed("time", true);
	return scorebox;
}


function refreshScore(svgarea) {
	console.log("d");
	svgarea.selectAll("text.score.team1").text(function(d) { d.g.team1.score += 1; return d.g.team1.score;});
}