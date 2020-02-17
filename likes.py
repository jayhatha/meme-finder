import tweepy 

import tweepy

ckey = 'Y365zdsa7dyqOy1RJ1eJu1eHw'
csecret = 'CJIu57sEbHdEf0MNddeYde5GjV2vGfJVN6Gqht9dThzuO0yg5f'
atoken = '943250878013652992-vT4fdk6C79BBshcFjK3GvatwBU4sCYm'
asecret = 'Mf5QepqocQU0b3LVzgbMNbEbuNJIsMiXmYlNkMVeWGriU'

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

stuff = tweepy.Cursor(api.favorites, id = '2224331', wait_on_rate_limit='true', wait_on_rate_limit_notify='true')

with open('likes.json', 'w') as outfile:
    for status in stuff.items(3200):
        try:
            outfile.write('{}\n'.format(status.text.encode("utf-8")))
        except UnicodeEncodeError as e:
            print(e)