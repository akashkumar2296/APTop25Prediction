import os
from flask import Flask, render_template, Response
from flask_cors import CORS
from flask_restful import Resource, Api
from model.Script_Final_Employed_Model_InProgress_Games_Week_13_Post_Process import Ranking_prediction



app = Flask(__name__, static_url_path="/static") 
api = Api(app)
CORS(app)

@app.route("/") 
def hello(): 
    return render_template("index.html")

class ApTop25Prediction(Resource):
	def get(self, team_name, quarter=None):
		ranking_tuple = Ranking_prediction(team_name)
		ranking_out = ""
		if quarter == None:
			ranking_out = ranking_tuple[3]
		else:
			quarter = int(quarter)
			if quarter < 5 and quarter > 0:
				ranking_out = ranking_tuple[quarter - 1]
			else:
				ranking_out = ranking_tuple[3]

		resp = Response(str(ranking_out))
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
		
api.add_resource(ApTop25Prediction, '/prediction/<string:team_name>', '/prediction/<string:team_name>/<string:quarter>', endpoint='app')


if (__name__ == "__main__"): 
    app.run(port = 5001) 