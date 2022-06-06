import twitter
import yfinance
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
import pytz
from requests import get
from bs4 import BeautifulSoup as bs
import json


def get_tweet_history(username):
    api_key = "l6W2qcWFlQIvj7wVbkQu4t9qo"
    api_key_secret = "NCu9kQIM8E0n16e1NBXVSFBbeq0ovcG9pQuo2oerNDNXg327To"
    access_token = "757375703809724416-Bjs7FAyO9e7qeUW7zVTWlU3e9ALuZPd"
    access_token_secret = "VlUNDQp5NvdidG1CSuy74mxiQAeQoJ2GqILf1Xsu4sPWU"

    api = twitter.Api(consumer_key=api_key,
                      consumer_secret=api_key_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

    tweets = api.GetUserTimeline(screen_name=username, include_rts=False, count=500)
    tweet_dict = {
        "Created At": [],
        "Tweet Text": []
    }
    for tweet in tweets:
        created_at = tweet.created_at
        created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        created_at = created_at - timedelta(hours=4)  # - 4 hrs for EST time
        created_at = datetime.strftime(created_at, "%Y-%m-%d %H:%M:00-04:00")
        tweet_dict["Created At"].append(created_at)
        tweet_dict["Tweet Text"].append(tweet.text)
    return tweet_dict


def write_tweets_to_db(username, tweet_dict):
    db_connection = create_engine('sqlite:///../db/base.db')
    data_frame = pd.DataFrame(tweet_dict)
    data_frame.to_sql(f"{username}_tweets", if_exists='replace', method='multi',
                      con=db_connection, chunksize=100, index=False)


def get_stock_data(ticker):
    db_connection = create_engine('sqlite:///../db/base.db')
    stock = yfinance.Ticker(ticker)
    # stock history for the past year in hour intervals
    data_frame = pd.DataFrame(stock.history(start="2019-10-03", end="2020-09-13", actions=False, interval="60m"))
    data_frame.index = pd.to_datetime(data_frame.index)
    data_frame.sort_index(inplace=True, ascending=False)
    data_frame.to_sql(f"elonmusk_fin_data", if_exists='replace', method='multi', con=db_connection, chunksize=100)
    print(data_frame)
    return data_frame


def go_get():
    import requests

    headers = {
        'authority': 'api.twitter.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-twitter-client-language': 'en',
        'x-csrf-token': '4dad92c7f1b5c22827bea2ccba3979f7',
        'x-guest-token': '1304981217931124737',
        'x-twitter-active-user': 'yes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://twitter.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://twitter.com/elonmusk/with_replies',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('include_want_retweets', '1'),
        ('tweet_mode', 'extended'),
        ('send_error_codes', 'true'),
        ('count', '20000')
    )

    response = requests.get('https://api.twitter.com/2/timeline/profile/44196397.json', headers=headers, params=params)

    return response
    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://api.twitter.com/2/timeline/profile/44196397.json?include_profile_interstitial_type=1^&include_blocking=1^&include_blocked_by=1^&include_followed_by=1^&include_want_retweets=1^&include_mute_edge=1^&include_can_dm=1^&include_can_media_tag=1^&skip_status=1^&cards_platform=Web-12^&include_cards=1^&include_ext_alt_text=true^&include_quote_count=true^&include_reply_count=1^&tweet_mode=extended^&include_entities=true^&include_user_entities=true^&include_ext_media_color=true^&include_ext_media_availability=true^&send_error_codes=true^&simple_quoted_tweet=true^&include_tweet_replies=true^&count=20^&userId=44196397^&ext=mediaStats^%^2ChighlightedLabel', headers=headers)


# page = go_get().text
# with open('thing.json', 'w+', encoding='utf-8') as file:
#     file.write(page)
# print(page)
# with open('thing.json', 'r+', encoding='utf-8') as file:
#     data = []
#     page = json.loads(file.read())
#     # print(len(page["globalObjects"]["tweets"]))
#     for item in page["globalObjects"]["tweets"].values():
#         # time_made = " ".join(item["created_at"].split()[:-2]) + " "
#         # time_made += " ".join(item["created_at"].split()[-1:])
#         data.append({
#             "Created At": item["created_at"],
#             "Tweet Link": f'https://twitter.com/elonmusk/status/{item["id_str"]}',
#             "Tweet Text": item["full_text"]
#         })
#     # df['Date'] = pd.to_datetime(df['Date'])
#     data_frame = pd.DataFrame(data)
#     data_frame["Created At"] = pd.to_datetime(data_frame["Created At"])
#     my_timezone = pytz.timezone('America/Toronto')
#     data_frame["Created At"] = data_frame["Created At"].dt.tz_convert(my_timezone)
#     data_frame.sort_values(by=["Created At"], inplace=True, ascending=False)
#     db_connection = create_engine('sqlite:///../db/base.db')
#     data_frame.to_sql(f"elonmusk_tweets", if_exists='replace', method='multi', con=db_connection, chunksize=100, index=False)
#     print(data_frame)
    # for tweet in page["globalObjects"]:
    #     print(tweet)
    # print(json.dumps(page, indent=2))
# js = json.loads(page)
# print(js["globalObjects"])
