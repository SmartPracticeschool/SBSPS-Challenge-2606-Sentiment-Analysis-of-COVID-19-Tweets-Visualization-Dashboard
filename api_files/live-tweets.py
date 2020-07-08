import tweepy
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import csv
import json
app = Flask(__name__)
CORS(app)
@app.route('/liveTweets',methods = ['GET','POST'])
def live_tweets():
     MAX_TWEETS = 10
     tweets=[]
     if request.method == 'POST':
         hashtag = request.args.get('hashtag')
     auth = tweepy.OAuthHandler('d2PWAgPJ46WALqw92JhVRdYue', 'WkoPasIYAwvJspylhr3bikyvkYCSgFhFbEqbqoF4Lk1cVQtKCe')
     auth.set_access_token("1010912451792195585-Oy9Xtv8kkm8kGPIwR8v6tuhPGkG4CZ","RtrZKT9mVhCLmGaSVN3t3f1oaudGdLeLLa98UuOKbQg3T")

     api = tweepy.API(auth)

     for tweet in tweepy.Cursor(api.search, q='#'+hashtag, rpp=100).items(MAX_TWEETS):
         tweets.append(tweet.text)

     return json.dumps({'tweets':tweets}), 200, {'ContentType':'application/json'} 

         

app.run()