1) data_download 
Downloading Geo data from https://crisisnlp.qcri.org/covid19 and saving it to Google Drive.
Umair Qazi, Muhammad Imran, Ferda Ofli. GeoCoV19: A Dataset of Hundreds of Millions of Multilingual COVID-19 Tweets with Location Information. ACM SIGSPATIAL Special, May 2020. doi: https://doi.org/10.1145/3404111.3404114 (ACM | arXiv | bibtex)
The data consists of only Tweet IDs and the geolocation of tweets as per the Twitter's content redistribution policy and hence the tweet IDs are hydrated in the further steps to obtain the full text of tweets.
Geodata Readme: https://crisisnlp.qcri.org/covid_data/geocov19_readme.txt
Keywords and Hashtags: https://crisisnlp.qcri.org/covid_data/COVID19_AIDR_Keywords.zip

2) data_extraction_india
Extracting Tweet IDs and Geolocation data from downloaded JSON files of tweets from Indian locations and saving them to text files

3) hydrate_tweet_IDs
Hydrating the Tweet IDs to obtain full tweet text and other required information and saving data to CSV files
Twarc is used for hydration of Tweet IDs
https://github.com/DocNow/twarc

4) merge_and_map
Merging the data and mapping the geodata from the text files to the tweet files.
