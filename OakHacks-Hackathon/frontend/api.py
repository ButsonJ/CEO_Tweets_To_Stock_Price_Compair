from flask import render_template, Flask, request, jsonify
from flask_cors import CORS
from time import time
import pandas as pd
from sqlalchemy import create_engine
from flask import jsonify


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

db_connection = create_engine('sqlite:///../db/base.db')


def get_fin_data(username):
    data_frame = pd.read_sql_table(f'{username}_fin_data', con=db_connection)
    data_frame = data_frame[["Datetime", "Close"]]
    data_frame.reset_index(drop=True, inplace=True)
    output = []
    for item in data_frame.values:
        output.append({
            "DateTime": item[0],
            "Close": item[1]
        })
    return output


def get_tweets(username):
    data_frame = pd.read_sql_table(f'{username}_tweets', con=db_connection)
    data_frame.reset_index(drop=True, inplace=True)
    output = []
    for item in data_frame.values:
        output.append({
            "CreatedAt": item[0],
            "TweetLink": item[1],
            "TweetText": item[2]
        })
    return output


@app.route('/api/v1/get_financial_data', methods=['GET'])
def return_fin_data():
    return jsonify(get_fin_data(request.args["username"]))


@app.route('/api/v1/get_tweets', methods=['GET'])
def return_tweets():
    return jsonify(get_tweets(request.args["username"]))


@app.route('/api/v1/search', methods=['GET'])
def search():
    return jsonify(get_tweets(request.args["query"]))


@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')



app.run()
