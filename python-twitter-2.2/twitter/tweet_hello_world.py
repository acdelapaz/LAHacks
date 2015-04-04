import twitter
# must save necessary keys in separate keys.txt file
keys = open('keys.txt', 'r')
key_list = keys.read().splitlines()
assert len(key_list) >= 4, "Error: missing keys"
consumer_key = key_list[0]
consumer_secret = key_list[1]
access_token = key_list[2]
access_token_secret = key_list[3]
api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)
api.PostUpdate("Hello world! #LAHacks")
