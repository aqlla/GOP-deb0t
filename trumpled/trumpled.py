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
    def __init__(self, api):
        super(MyStreamListener, self).__init__()
        self.api = api
        self.tweets = []

    def on_data(self, data):
        json_data = json.loads(data)
        # if 'limit' in json_data.keys():
        #     try:
        #         res = api.search(q='donald trump', count=100)
        #         write_to_file(str(res))
        #     except tweepy.TweepError as e:
        #         print(e)
        if 'retweeted' not in json_data.keys() or not json_data['retweeted'] and not json_data['text'].startswith('RT'):
            if 'text' in json_data.keys():
                print('@' + json_data['user']['screen_name'] + ': ' + json_data['text'])
                if 'masturbat' in str(json_data['text']) or 'circle jerk' in str(json_data['text']):
                    try:
                        t = "RT @" + json_data['user']['screen_name'] + ': ' + json_data['text'] + " #gopdeb0t"
                        api.update_status(status=t)
                    except tweepy.TweepError as e:
                        print(e)
            self.addtweet(json_data)
            return True


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

myStreamListener = MyStreamListener(api)
stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
stream.filter(track=['donald trump', 'gop', 'debate', 'GOPdebate', 'donaldtrump', 'rand paul', 'randpaul', 'jeb bush', 'ted cruz', 'carly fiorina', 'carlyfiorina', 'ronald regan', 'israel debate', 'hillary debate', 'terrorism debate', 'terrorist debate', 'palestine', 'obama debate', 'mexicans debate', 'anchor babies', 'illegal immigrants', 'ben carson', 'chris christie', 'marco rubio', 'jebbush', 'ronaldregan'], async=True)
