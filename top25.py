import os
from flask import Flask, render_template, Response
from flask_cors import CORS
from flask_restful import Resource, Api
from model.Script_Final_Employed_Model_InProgress_Games_Week_13 import Ranking_prediction



app = Flask(__name__, static_url_path="/static") 
api = Api(app)
CORS(app)

@app.route("/") 
def hello(): 
    return render_template("index.html")

class ApTop25Prediction(Resource):
	def get(self, team_name):
		resp = Response(str(Ranking_prediction(team_name)))
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

api.add_resource(ApTop25Prediction, '/prediction/<string:team_name>')


if (__name__ == "__main__"): 
    app.run(port = 5001) 