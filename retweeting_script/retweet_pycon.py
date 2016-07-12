import tweepy
import os
import ConfigParser
import sys

debug = True
config_file = "config.ini"
config_path = os.path.join(os.path.expanduser('~'), config_file)


def parser_cfg():
    """
    Helper function to parser configuration file related
    Twitter OAuth Token
    """
    global config_path
    config = ConfigParser.ConfigParser()
    cfg = {}

    if not os.path.exists(config_path):
        print("Trying local configuration file")
        config_path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(config_path):
            sys.exit("Unable to find configuration file %s" % config_path)

    if debug:
        print("Using configuration file from %s" % config_path)

    config.read(config_path)
    cfg["consumer_key"] = config.get("twitter_auth_config", "consumer_key")
    cfg["consumer_secret"] = config.get("twitter_auth_config",
                                        "consumer_secret")
    cfg["access_token"] = config.get("twitter_auth_config", "access_token")
    cfg["access_token_secret"] = config.get("twitter_auth_config",
                                            "access_token_secret")
    return cfg


def get_api(cfg):
    """
    Helper function get Tweepy API
    params: config dictionary containing Twitter OAuth tokens
    returns: tweepy API object
    """
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    """ Main function """
    cfg = parser_cfg()
    api = get_api(cfg)
    while True:
        for status in api.user_timeline('pyconindia'):
            current_status_id = status.id
            print current_status_id
            break
        retweet_status = api.get_status(current_status_id).retweeted
        print retweet_status
        if retweet_status:
            print("already retwitted")
        else:
            print("retweeting")
            api.retweet(current_status_id)

if __name__ == "__main__":
    main()
