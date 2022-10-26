import json
import gzip
import os

def get_text(tweet):
	try:
		text = tweet['extended_tweet']['full_text']
	except:
		text = tweet['text']
	return text


def get_hashtag(tweet):
	try:
		hashtags = tweet['extended_tweet']['entities']['hashtags']
	except:
		hashtags = tweet['entities']['hashtags']
	return [hashtag['text'] for hashtag in hashtags]


def clean_text(text):
	words = text.split()
	words2 = []
	for i in words:
		if 'http' not in i and '\\' not in i:
			words2.append(i)
		if '\\u2019' in i:
			words2.append(i.replace('\u2019','\''))
	for i in words2[::-1]:
		if '#' in i:
			words2.remove(i)
		if '#' not in i:
			break
	sentence = ''
	for i in words2:
		sentence = sentence+i+' '
	sentence = sentence.replace('#','')
	return sentence


year = '2022'
for month in range(1,13):
	month = "%02d" % (month,)
	b = os.listdir(year + '-' + month)
	try:
		c=os.listdir(year + '-' + month + '-clean')
	except:
		os.system('mkdir ' + year + '-' + month + '-clean')
	b.sort()
	for j in b:
		if 'jsonl.gz' not in j:
			continue
		if j in c:
			continue
		print(j)
		try:
			tweets = gzip.open(year + '-' + month + '/' + j).read().decode().split('\n')[:-1]
		except:
			f = open('log_clean.txt','a')
			x = f.write(j+' is broken!'+'\n')
			f.close()
			continue
		f = gzip.open(year + '-' + month + '-clean/' + j, 'a')
		f2 = gzip.open(year + '-' + month + '.jsonl.gz', 'a')
		for i in tweets:
			tweet = json.loads(i)
			if tweet['lang'] != 'en':
				continue
			if 'retweeted_status' in tweet.keys():
				continue
			cleaned_tweet = {}
			cleaned_tweet['text'] = clean_text(get_text(tweet))
			cleaned_tweet['id'] = tweet['id']
			cleaned_tweet['time'] = tweet['created_at']
			cleaned_tweet['user'] = tweet['user']['id']
			cleaned_tweet['hashtags'] = get_hashtag(tweet)
			x = f.write((json.dumps(cleaned_tweet) + '\n').encode())
			x = f2.write((json.dumps(cleaned_tweet) + '\n').encode())
		f.close()
		f2.close()
		del tweets
