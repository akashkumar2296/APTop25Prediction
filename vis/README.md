
Notes on the AP Top 25 Prediction Visualization
===============================================

How to run the page
----------------------

You need to host the html in a web server in order to render the images properly.  You may use python -m http.server to serve the html - see HW2 instructions.

Notes
-----

1. The visualization is driven from a grid that shows the Top 25 rankings by week - 16 rows (weeks) by 25 teams (in ranking order)

2. College logo images are used to represent the teams - this is an effective and widely used presentation of the college teams.

3. Actual AP rankings are shown on somewhat de-emphasized in light gray background while the predictions highlighted in cyan.

4. Hovering over a team icon will bring up a tooltip window that can show the key statistics for that team and week.

5. We may also show some graphical representations of data on mouseover.

6. *At this point, we need some feedback from the team to nail down the visualization features*

7. The js has been developed so that it is ready to be hooked up to some real datasets.  For now, the rankings are randomly generated and the number of weeks to show hard-coded.  These are very easy to fix once we can hook it up to the actual datasets and prediction model.

