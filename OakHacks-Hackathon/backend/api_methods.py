import pandas as pd
from sqlalchemy import create_engine
from flask import jsonify

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

# print(get_tweets('elonmusk'))