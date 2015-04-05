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
api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)
try:
	f = open('save.p', 'rb')
	lastid = pickle.load(f)
	f.close()
except IOException as e: 
	lastid = None
mentions_list = api.GetMentions(None, lastid)
def statify(user):
	username = user.GetScreenName()
	followers = user.GetFollowersCount()
	statlist = api.GetUserTimeline(user.GetId(), None, None, None, 10, False, None, False)
	# statlist = api.GetUserTimeLine(user)
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
	rt_ratio = round(avg_rts/float(followers) * 100, 2)
	fav_ratio = round(avg_favs/float(followers) * 100, 2)
	api.PostUpdate("@" + username + " Data for last 10 tweets\n" + "Average RTs: {}".format(avg_rts) + "\nAverage favs: {}\n".format(avg_favs) + "Follower RT pct: {}%".format(rt_ratio) + "\nFollower fav pct: {}%".format(fav_ratio))

for tweet in mentions_list:
	tweettxt = tweet.GetText()
	if "StatifyMe!" in tweettxt:
		f = open('save.p', 'wb')
		pickle.dump(tweet.GetId(), f)
		f.close()
		statify(tweet.GetUser())
		
