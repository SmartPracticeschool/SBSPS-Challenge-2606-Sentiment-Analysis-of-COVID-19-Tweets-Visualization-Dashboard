Python Flask REST APIs were created for Live Sentiment Analysis and Predictive Analytics of sentiment of people if Government decides to extend the lockdown.

API has 2 endpoints:

1)<b>/predict:</b>

/predict accepts a POST or a GET request from the web node application and returns daily positivity score (indicating rise and fall of positivity among people regarding lockdown) in JSON format. This response is then presented as line graph on the visualization dashboard. The response includes dates from 01 February 2020 till current date. The value plotted each day indicates how positive the people will be if the government decides to extend the lockdown.

2)<b>/liveTweets:</b>

/liveTweets accepts a POST or a GET request from the web node application along with the hashtags/keywords provided by the user according to the topics on which the user requires analysis. It returns response in JSON format which is then presented on the visualization dashboard. Tweets, Sentiment analysis on the tweets and the word cloud is provided to the user on the dashborad for the topic provided by the user.

The API code and the dependent files are available in this folder.
