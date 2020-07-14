import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#getting set of stopwords in English
stop_words = set(stopwords.words('english'))
def clean_tweet(tweet):
  tweet=bs4.BeautifulSoup(tweet,'lxml').get_text()

  #removing mentions
  tweet=re.sub(r'@[A-Za-z0-9]+',' ',tweet)

  #removing URLs
  tweet=re.sub(r'https?://[A-Za-z0-9./]+',' ',tweet)

  #removing characters other than english alphabets 
  tweet=re.sub(r"[^a-zA-Z']",' ',tweet)

  #removing extra white spaces
  tweet=re.sub(r" +"," ",tweet)

  #removing leading and trailing white spaces
  tweet=tweet.strip()

  #converting text to lowercase
  tweet=tweet.lower()

  #Tokenizing Tweer
  word_tokens = word_tokenize(tweet)

  #removing stopwords
  filtered_tweet = [w for w in word_tokens if not w in stop_words]
  return ' '.join(filtered_tweet)
