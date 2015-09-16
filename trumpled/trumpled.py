from time import gmtime, strftime
import tweepy
import codecs
import json
import sys

consumer_key = "iknQUv5yjPnyn5N0CbUdmDRt4"
consumer_secret = "H82FgoGFJfRjpU2S74FbEnAzFVTHBy0izqYVR832YaBr9gZxNT"
access_token = "244758828-IgAmPKt2iY1wrdSzLyqKGLAseZSdVd9a2poNbCkn"
access_secret = "Xeyf2lTykUcGqaAWehy6x5pqV5JtQ33uO8zmGu2LZi31r"


class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super(MyStreamListener, self).__init__()
        self.tweets = []

    def on_data(self, data):
        json_data = json.loads(data)
        if 'retweeted' not in json_data.keys() or not json_data['retweeted'] and not json_data['text'].startswith('RT'):
            return self.addtweet(json_data)

    def on_error(self, status_code):
        print('stream listener: ', status_code)
        if status_code == 420:
            return True

    def addtweet(self, tweet):
        self.tweets.append(tweet)
        if len(self.tweets) >= 100:
            write_to_file(self.tweets)
            self.tweets = []
            return True

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True



def authenticate_app():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)

def write_to_file(tweets):
    timestr = strftime("%Y%m%d-%H%M%S", gmtime())

    try:
        with codecs.open(timestr + ".json", 'w') as fp:
            json.dump(tweets, fp=fp, indent=2, ensure_ascii=False)
            return True
    except IOError as e:
        print(e)
        return False




api = authenticate_app()

# results = api.search(q="trump", count=100)
# write_to_file(results)

myStreamListener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
stream.filter(track=['trump', '#GOPdebate'], async=True)
