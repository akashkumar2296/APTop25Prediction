var aprankings = new Array();
wkfake =["washingtonst","clemson","notredame","michigan","georgia","oklahoma","westvirginia","ohiostate","lsu","alabama","ucf","kentucky","syracuse","utahstate","texas","fresnostate","bostoncollege","msstate","florida","washington","pennstate","ncstate","iowastate","msstate","cincinnati"]
wk11 =["alabama","clemson","notredame","michigan","georgia","oklahoma","westvirginia","ohiostate","lsu","washingtonst","ucf","kentucky","syracuse","utahstate","texas","fresnostate","bostoncollege","msstate","florida","washington","pennstate","ncstate","iowastate","msstate","cincinnati"]
wk12 = ["alabama","clemson","notredame","michigan","georgia","oklahoma","westvirginia","washingtonst","ohiostate","lsu","ucf","syracuse","texas","utahstate","florida","pennstate","washington","iowastate","cincinnati","kentucky","utah","bostoncollege","boisestate","northwestern","msstate"]

for (var i=1; i <= getCurrentWeek(); i++) {
    var thisweek;
    try {
        thisweek = eval("wk"+i);
    } catch (error) {
        thisweek = wkfake;
    }
    aprankings.push(thisweek); 
}
