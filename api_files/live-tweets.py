import tweepy
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import csv
import json
import bs4
import re
import ktrain
import joblib
from datetime import timedelta
import pandas as pd
import numpy as np
import requests
from datetime import datetime

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

         
@app.route('/predict',methods=['GET','POST'])
def lockdownPrediction():
        today=datetime.today().strftime('%d-%m-%Y')
        s_date=datetime.strptime('03-07-2020','%d-%m-%Y')
        e_date=datetime.strptime(today,'%d-%m-%Y')
        dates=pd.date_range(s_date,e_date,freq='d')
        case_dates=[]
        for d in dates:
            d1 = d - timedelta(days=2)
            d2=d1.strftime('%d-%m-%Y')
            case_dates.append(d2)
        x= requests.get('https://api.covid19india.org/data.json')
        data_stats = x.json()
        data = data_stats["cases_time_series"]
        confirmed=[]
        active=[]
        death=[]
        recovered=[]
        date=[]
        print(case_dates)
        for i in data:
            confirmed.append(i["dailyconfirmed"])
            death.append(i["dailydeceased"])
            recovered.append(i["dailyrecovered"])
            date.append(i["date"])
            activee=int(i["dailyconfirmed"])-(int(i["dailydeceased"])+int(i["dailyrecovered"]))
            active.append(activee)
        cases=pd.DataFrame()
        cases['date']=date
        cases['confirmed']=confirmed
        cases['active']=active
        cases['death']=death
        cases['recovered']=recovered

        cdates=[]
        for d in cases['date']:
            d1=d.strip()+' 2020'
            d2=datetime.strptime(d1,'%d %B %Y').strftime('%d-%m-%Y')
            cdates.append(d2)
        cases['date']=cdates
        cases1=cases[cases['date'].isin(case_dates)]
        
        gbr=joblib.load('grad.sav')
        y=gbr.predict(cases1.iloc[:,[1,2,3,4]])
        output=pd.DataFrame()
        fd=[]
        for i in range(len(dates)):
             d=dates[i]
             d1=d.strftime('%d-%m-%Y')
             fd.append(str(d1))
            
        output['sentiment_date']=fd
        output['sentiment_score']=y
        
        output['case_date']=cases1['date']

        output['confirmed']=cases1['confirmed']
        output['active']=cases1['active']
        output['death']=cases1['death']
        output['recovered']=cases1['recovered']

        
        output=output.reset_index(drop=True)
        print(output.head())
        original = pd.read_csv('/home/rahul/Sentiment-Analysis/public/predict - full.csv')
        frames = [original,output]
        final_pd = pd.DataFrame()
        final_pd = pd.concat(frames)
        final_pd.to_csv('/home/rahul/Sentiment-Analysis/public/final_lockdown_pred.csv',index=False)

        return 'OK'

app.run()