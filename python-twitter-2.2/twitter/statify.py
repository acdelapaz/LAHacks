import twitter
import cPickle as pickle

# must save necessary keys in separate keys.txt file
keys = open('statifykeys.txt', 'r')
key_list = keys.read().splitlines()
assert len(key_list) >= 4, "Error: missing keys"
consumer_key = key_list[0]
consumer_secret = key_list[1]
access_token = key_list[2]
access_token_secret = key_list[3]
#Connects @Statify_Tweets to Twitter API
api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)
#Checking for pickle file
try:
	f = open('save.p', 'rb')
	#lastid prevents duplicate responses to old mentions by tracking the last mention that was successfully statified
	lastid = pickle.load(f)
	f.close()
except IOException as e: 
	lastid = None
#ignores mentions before lastid
mentions_list = api.GetMentions(None, lastid)

def statify(user):
	username = user.GetScreenName()
	followers = user.GetFollowersCount()
	#Gets previous 10 tweets from user, including mentions but not including retweets
	statlist = api.GetUserTimeline(user.GetId(), None, None, None, 10, False, None, False)
	if len(statlist) == 0:
		return
	rts = 0
	favs = 0
	for status in statlist:
		print(status.GetText())
		rts += status.GetRetweetCount()
		favs += status.GetFavoriteCount()
	avg_rts = round(rts/float(len(statlist)), 2)
	avg_favs = round(favs/float(len(statlist)), 2)
	#rt_ratio and fav_ratio get the ratio of average retweets/favorites to the number of the user's followers. Represented as a percentage of followers.
	rt_ratio = round(avg_rts/float(followers) * 100, 2)
	fav_ratio = round(avg_favs/float(followers) * 100, 2)
	#tweets data
	api.PostUpdate("@" + username + " Data for last 10 tweets\n" + "Average RTs: {}".format(avg_rts) + "\nAverage favs: {}\n".format(avg_favs) + "Follower RT pct: {}%".format(rt_ratio) + "\nFollower fav pct: {}%".format(fav_ratio))

#iterates through all new mentions
for tweet in mentions_list:
	tweettxt = tweet.GetText()
	#tweet must contain phrase "StatifyMe!" and must mention @Statify_Tweets in order for the user to get tweet statistics
	if "StatifyMe!" in tweettxt:
		f = open('save.p', 'wb')
		#serializes ID of last tweet to be statified
		pickle.dump(tweet.GetId(), f)
		f.close()
		statify(tweet.GetUser())	
