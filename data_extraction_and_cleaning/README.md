<b>Extraction of Tweet IDs and Geodata:</b>

Geo data is downloaded from https://crisisnlp.qcri.org/covid19.
The data consists of only Tweet IDs and the geolocation of tweets as per the Twitter's content redistribution policy and hence the tweet IDs are hydrated in the further steps to obtain the full text of tweets.
Keywords and Hashtags included can be fount at: https://crisisnlp.qcri.org/covid_data/COVID19_AIDR_Keywords.zip

<b>Filtering Tweet IDs that include only Indian locations:</b>

The geodata is used to filter tweets from Indian locations.</b>

<b>Hydration of Tweet IDs:</b>

In order to obtain full tweet text and other tweet data, we hydrate the tweet IDs.
Tool used for this purpose is Twarc which can be found at : https://github.com/DocNow/twarc

<b>Mapping of Geodata to Tweet Data:</b>

Mapping of geodata to the tweet data to create the final dataset

<b>Cleaning:</b>

It invovles cleaning of tweets by removing characters other than English alphabets, removing mentions and URLs, Stop word removal, Tokenization, etc to produce cleaned tweets.

