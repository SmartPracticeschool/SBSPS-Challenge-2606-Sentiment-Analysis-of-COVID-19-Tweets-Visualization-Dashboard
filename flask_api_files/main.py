import tweepy
from flask import Flask,request,jsonify
from flask_cors import CORS
import bs4
import re

import joblib
from datetime import timedelta
import pandas as pd
import requests
from datetime import datetime
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
app = Flask(__name__)
cors=CORS(app)
@app.route('/liveTweets',methods = ['GET','POST'])
def live_tweets():
     MAX_TWEETS = 100
     tweets=[]
     if request.method == 'POST':
         hashtag = request.args.get('hashtag')
     auth = tweepy.OAuthHandler('d2PWAgPJ46WALqw92JhVRdYue', 'WkoPasIYAwvJspylhr3bikyvkYCSgFhFbEqbqoF4Lk1cVQtKCe')
     auth.set_access_token("1010912451792195585-Oy9Xtv8kkm8kGPIwR8v6tuhPGkG4CZ","RtrZKT9mVhCLmGaSVN3t3f1oaudGdLeLLa98UuOKbQg3T")

     api = tweepy.API(auth)

     for tweet in tweepy.Cursor(api.search, q='#'+hashtag, rpp=100).items(MAX_TWEETS):
         tweets.append(tweet.text)

     cleaned_tweets = []
     para=''
     stop_words = set(stopwords.words('english'))
     for tweet in tweets:
        tweet=bs4.BeautifulSoup(tweet,'lxml').get_text()
        tweet=re.sub(r'@[A-Za-z0-9]+',' ',tweet)
        tweet=re.sub(r'https?://[A-Za-z0-9./]+',' ',tweet)
        tweet=re.sub(r"[^a-zA-Z']",' ',tweet)
        tweet = re.sub(r'&amp;', '&', tweet)
        tweet=re.sub(r" +"," ",tweet)
        tweet=tweet.strip()
        #tweet=tweet.lower()
        #word_tokens = word_tokenize(tweet)
        #filtered_tweet = [w for w in word_tokens if not w in stop_words]
        #return ' '.join(filtered_tweet)
        #print(tweet)
        cleaned_tweets.append(tweet)
        para=para+tweet
     stop_words = set(stopwords.words('english'))

     para=para.replace('\n',' ')
     para=para.replace('\r','')
     para=bs4.BeautifulSoup(para,'lxml').get_text()
     para=re.sub(r'@[A-Za-z0-9]+',' ',para)
     para=re.sub(r'https?://[A-Za-z0-9./]+',' ',para)
     para=re.sub(r"[^a-zA-Z']",' ',para)
     para=re.sub(r" +"," ",para)
     para=para.strip()
     para=para.lower()
     word_tokens = word_tokenize(para)
     filtered_tweet = [w for w in word_tokens if not w in stop_words]
     para=' '.join(filtered_tweet)

     from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
     analyser = SentimentIntensityAnalyzer()
     def sentiment_analyzer_scores(sentence):
         score = analyser.polarity_scores(sentence)
         sentiments = score['compound']
         return sentiments
     sentiment =[]
     df=pd.DataFrame(cleaned_tweets,columns=['text'])
     for s in df['text']:
         senti = sentiment_analyzer_scores(s)
         sentiment.append(senti)
     df['sentiment'] = sentiment

     def label(sentiment_value):
	     if(sentiment_value>=0.05):
	 	     return 1
	     elif(sentiment_value<=-0.05):
		     return -1
	     else:
		     return 0
     df['sentiment_label']=df['sentiment'].apply(label)
     pos=0
     neg=0
     neu=0
     count=[]
     sentimentt=[]
     text=[]
     sent=[]
     for x in df['sentiment_label']:
         if x==1:
             pos=pos+1
             sent.append('Positive')
             text.append(df['text'])
         elif x==-1:
             neg=neg+1
             sent.append('Negative')
             text.append(df['text'])
         else:
             neu=neu+1
             sent.append('Neutral')
             text.append(df['text'])
     count.append(pos)
     count.append(neg)
     count.append(neu)
     sentimentt.append('Positive')
     sentimentt.append('Negative')
     sentimentt.append('Neutral')
     #df1=pd.DataFrame(sentimentt,columns=['Sentiment'])
     #df2=pd.DataFrame(count,columns=['Count'])
     #dff=pd.concat([df1,df2],axis=1,ignore_index=True)
     #dff.to_csv('count.csv',index = False)
     #stt='success'
     df['Sentiment']=sent
     df_table=df[['text','Sentiment']]
     #df_table.to_csv('tweet_table.csv')
     tweets_dict={}
     tweets_dict['para']=para
     tweets_dict['positive']=pos
     tweets_dict['negative']=neg
     tweets_dict['neutral']=neu
     tweets_dict['text']=list(df_table['text'])
     tweets_dict['Sentiment']=list(df_table['Sentiment'])


     return jsonify({'prediction': tweets_dict})


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

        cases1=cases1.reset_index(drop=True)
        output['case_date']=cases1['date']
        output['confirmed']=cases1['confirmed']
        output['active']=cases1['active']
        output['death']=cases1['death']
        output['recovered']=cases1['recovered']
        output['sentiment_date']=fd
        output['sentiment_score']=y


        output=output.reset_index(drop=True)
        print(output.head())
        original = pd.read_csv('predict - full.csv')

        frames = [original,output]
        final_pd = pd.DataFrame()
        final_pd = pd.concat(frames)
        print(final_pd.tail())
        final_dict={}
        final_dict['case_date']=list(final_pd['case_date'])
        final_dict['confirmed']=list(final_pd['confirmed'].astype('int64'))
        final_dict['active']=list(final_pd['active'].astype('int64'))
        final_dict['death']=list(final_pd['death'].astype('int64'))
        final_dict['recovered']=list(final_pd['recovered'].astype('int64'))
        final_dict['sentiment_date']=list(final_pd['sentiment_date'])
        final_dict['sentiment_score']=list(final_pd['sentiment_score'].astype('float'))
        #final_pd.to_csv('final_lockdown_pred.csv',index=False)

        return jsonify({'prediction': final_dict})
if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 5000 # If you don't provide any port the port will be set to 12345

    #model = joblib.load("soil_clustering.pkl") # Load "model.pkl"
    #print ('Model loaded')
    app.run(port=port, debug=True)
