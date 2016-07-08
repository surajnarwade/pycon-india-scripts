import tweepy
import ConfigParser
import json
import bitly_api
import time
import os

config = ConfigParser.ConfigParser()
config.read('config.ini')
consumer_key = config.get('twitter_auth_config', 'consumer_key')
consumer_secret = config.get('twitter_auth_config', 'consumer_secret')
access_token = config.get('twitter_auth_config', 'access_token')
access_token_secret = config.get('twitter_auth_config', 'access_token_secret')
bitly_access_token = config.get('bitly_auth_config','access_token')
conn_btly = bitly_api.Connection(access_token=bitly_access_token)

def create_json_file():
    if os.path.isfile('result.json'):
        print('result.json is already present')
    else:
        import pyconspider
    with open('result.json') as data_file:
        data = json.load(data_file)
    return data

def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def main():
    data = create_json_file()
    api = get_api()
    for i in data:
        clicks = conn_btly.shorten(i['link'].strip())
        tweet = "%s by %s, click here %s to vote:\n @pyconindia" % (i['title'].strip()[0:58]+'...', i['author'].split("(")[0].strip(), clicks['url'])
        #print tweet
        status = api.update_status(status=tweet)
        time.sleep(7200)

if __name__ == "__main__":
    main()
