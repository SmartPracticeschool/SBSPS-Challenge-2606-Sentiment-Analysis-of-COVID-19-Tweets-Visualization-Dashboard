from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#Assigning Vader Compound scores to each tweet
def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    sentiment_positivity_score = score['compound']
    return sentiment_positivity_score

#Assigning Vader Sentiment Label(positive,negative,neutral) to each tweet
# 1:posiitve
# -1:negative
# 0:neutral
def sentiment_analyzer_label(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    sentiment_positivity_score = score['compound']
    if(sentiment_positivity_score >=0.05):
        return 1
    elif(sentiment_positivity_score <=0.05):
        return -1
    else:
        return 0
    
    


