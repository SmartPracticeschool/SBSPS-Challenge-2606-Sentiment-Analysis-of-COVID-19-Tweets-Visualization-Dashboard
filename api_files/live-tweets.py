import tweepy
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import csv
import json
import bs4
import re
import ktrain
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
     #print(tweets)
     cleaned_tweets = []
     for tweet in tweets:
        tweet=bs4.BeautifulSoup(tweet,'lxml').get_text()
        tweet=re.sub(r'@[A-Za-z0-9]+',' ',tweet)
        tweet=re.sub(r'https?://[A-Za-z0-9./]+',' ',tweet)
        tweet = re.sub(r'&amp;', '&', tweet)
        #tweet=re.sub(r"[^a-zA-Z']",' ',tweet)
        tweet=re.sub(r" +"," ",tweet)
        tweet=tweet.strip()
        #tweet=tweet.lower()
        #word_tokens = word_tokenize(tweet)
        #filtered_tweet = [w for w in word_tokens if not w in stop_words]
        #return ' '.join(filtered_tweet)
        #print(tweet)
        cleaned_tweets.append(tweet)
     #print(cleaned_tweets)
        y = {} 
     predictor= ktrain.load_predictor('/home/rahul/Sentiment-Analysis/bert_model3/')
     for x in cleaned_tweets:
        sentiments = predictor.predict(x)
        if sentiments in y:
            y[sentiments]+=1
        else:
            y[sentiments] = 1

     import csv
     with open('/home/rahul/Sentiment-Analysis/public/livesentiments.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sentiment","Count"])
        for key in y:
            writer.writerow([key,y[key]])


     return y, 200, {'ContentType':'application/json'} 

         

app.run()