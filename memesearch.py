# importing all our tweepy and nltk requirements
# fyi i borrowed some of this from marco bonzanini (https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/)
import os
import tweepy
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import operator
import string
import re
import nltk
import pandas
from nltk.collocations import *
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import stem
from collections import defaultdict
import flask
from flask import render_template
nltk.download('wordnet')
app = flask.Flask(__name__)
lemmatizer = nltk.stem.WordNetLemmatizer()
# access tokens go here
MY_CONSUMER_KEY = os.environ.get('MY_CONSUMER_KEY')
MY_CONSUMER_SECRET = os.environ.get('MY_CONSUMER_SECRET')
MY_ACCESS_TOKEN_KEY = os.environ.get('MY_ACCESS_TOKEN_KEY')
MY_ACCESS_TOKEN_SECRET = os.environ.get('MY_ACCESS_TOKEN_SECRET')
# authenticating w/ twitter api
auth = tweepy.OAuthHandler(MY_CONSUMER_KEY, MY_CONSUMER_SECRET)
auth.set_access_token(MY_ACCESS_TOKEN_KEY, MY_ACCESS_TOKEN_SECRET)
# searching multiple pages
api = tweepy.API(auth)
query = '\"these * memes\" OR \"these * * memes\" OR \"the * meme is\" OR \"that * meme\" OR \"meme except\" OR \"meme needs to\" OR \"a meme now\" -rt -@ -http -#dad -.com -ift -filter:replies'
max_tweets = 10000
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(
            last_id - 1), result_type='recent', lang='en', wait_on_rate_limit='true', wait_on_rate_limit_notify='true')
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # in case something goes wrong
        break
punctuation = list(string.punctuation)
extrastops = open('stopwords.txt', 'r').read().split()
stop = stopwords.words('english') + punctuation + extrastops
# dumping our tweets to a json file
with open('tweets.json', 'w') as outfile:
    for tweet in searched_tweets:
        try:
            outfile.write('{}\n'.format(tweet.text.encode("utf-8")))
        except UnicodeEncodeError as e:
            print(e)
    """
    #finding bigrams and trigrams in our tweets
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(results)
    print('collocations:')
    print(finder.nbest(bigram_measures.pmi, 10))  # doctest: +NORMALIZE_WHITESPACE
"""
# getting just the text of the tweets, i think?
"""
with open('tweets.json', 'r') as f:
    for line in f:
        tw = TweetTokenizer()
        tweet = json.loads(line)
        keys = tweet.keys()
        array_length = len(results['statuses'])
        print('collected ' + str(array_length) + ' tweets')
        #print('likely memes:')
        with open('rawtext.json', 'w') as a, open('xmeme.json', 'w') as b:
            for i in range(array_length):
                rawtext = (results['statuses'][i]['text'])
                json.dump(rawtext, a)

                #finding words in front of 'meme'
with open('tweets.json', "r") as readfile:
    target = "meme"
    words = (line.split('\n') for line in readfile)
    for i,w in enumerate(words):
        if w == target:
            if i>0:
                xmeme = (words[i-3] + ' ' + words[i-2] + ' ' + words[i-1])
                print(words)


        #finding phrases between 'the' and 'meme'
        with open('rawtext.json', 'r') as f:
            data = f.read()
            x = re.findall(r'the(.*?)meme', data, re.DOTALL)
            match_x = re.findall(r'(?<![@])\b[a-zA-Z]{3,15}\b', str(x))
            filtered_x = [term for term in match_x if term not in stop]
            bigram_measures = nltk.collocations.BigramAssocMeasures()
            trigram_measures = nltk.collocations.TrigramAssocMeasures()
            finder = BigramCollocationFinder.from_words(filtered_x)
            finder = TrigramCollocationFinder.from_words(filtered_x)
            print('collocations:')
            finder = BigramCollocationFinder.from_words(filtered_x)
            print(finder.nbest(bigram_measures.pmi,
                               20))  # doctest: +NORMALIZE_WHITESPACE
            finder = TrigramCollocationFinder.from_words(filtered_x)
            print(finder.nbest(trigram_measures.pmi,
                               20))  # doctest: +NORMALIZE_WHITESPACE
            print(x)
        #tokenizing our tweets
        with open('tokens.json', 'w') as outfile:
            for i in range(array_length):
                #print (results['statuses'][i]['text'])
                tokens = tw.tokenize(results['statuses'][i]['text'])
                json.dump(tokens, outfile)
            print('tokenized tweets')

        #tokens = tw.tokenize(tweet["text"])

frequency = {}
"""
# converting our meme terms to twitter queries


def toLink(a):
    b = '<a href="https://twitter.com/search?l=en&q=' + a + 'lang=en\"</a>'
    return b


# counting word frequencies
count_all = Counter()
document_text = open('tweets.json', 'r')
text_string = document_text.read().lower()
match_pattern = re.findall(r'(?<![@])\b[a-zA-Z]{3,15}\b', text_string)
filtered_words = [term for term in match_pattern if term not in stop]
lemmas = [lemmatizer.lemmatize(t) for t in filtered_words]
# counting pairs
pairs = bigrams(lemmas)
count_all.update(pairs)
#print('most common pairs:')
pairs = (count_all.most_common(25))
# print(count_all.most_common(25))
# resetting counter and counting single words
count_all = Counter()
count_all.update(lemmas)
#print('most common words:')
memes = (count_all.most_common(50))
# making dataframes for our memes and pairs
memedf = pandas.DataFrame(memes, columns=['term', 'count'])
pairdf = pandas.DataFrame(pairs, columns=['term', 'count'])
#memedf['term'] = memedf['term'].apply(toLink)
# turning them into html tables
memetable = memedf.to_html(escape=False)
pairtable = pairdf.to_html(escape=False)


# print(count_all.most_common(50))
# print(pairs)
# print(memes)


# rendering tables that will show up on index.html
@app.route('/')
def index():
    return render_template('index.html', memes=memes, pairs=pairs, memetable=memetable, pairtable=pairtable)


if __name__ == "__main__":
    app.run(debug=True)

"""
#counting words right before 'meme
xmeme_text = open('tweets.json', 'r')
xmeme_string = xmeme_text.read().lower()
xmeme_pattern = re.findall(r'(?<![@])\b[a-zA-Z]{3,15}\b', xmeme_string)
filtered_xmeme = [term for term in xmeme_pattern if term not in stop]
count_all = Counter()
count_all.update(filtered_xmeme)
print ('upcoming memes')
print(count_all.most_common(20))
xpairs = bigrams(filtered_xmeme)
count_all = Counter()
count_all.update(xpairs)
print(count_all.most_common(5))



#find words that occur together
com = defaultdict(lambda : defaultdict(int))
for i in range(len(filtered_words)-1):
        for j in range(i+1, len(filtered_words)):
            w1, w2 = sorted([filtered_words[i], filtered_words[j]])
            if w1 != w2:
                com[w1][w2] += 1
com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:20])

#set up data for bar graph
count_all = Counter()
count_all.update(filtered_words)
word_freq = count_all.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')
"""
