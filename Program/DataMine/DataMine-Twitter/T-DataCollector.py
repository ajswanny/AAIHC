import tweepy, textblob

# [START Authentication]

# Create the necessary authentication data.
consumer_key = 'YdjsLPhVFR2m3zcxMZz6LrKNS'
consumer_secret = 'biTJRckxB6RKhAhzYA2tM8GI7jpA0ZFpWkd2XeLIP6EcLMqkyv'

access_token = '783145791468822528-GkYMR3ApZ0trEH7Do0supAdgiH9PrgE'
access_token_secret = 'aDHykUZ2Ipcu7reOwTRaXox8JuZY9V4j58Q1NVE85giEW'

# Create authentication handler.
authentication = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

authentication.set_access_token(key=access_token, secret=access_token_secret)

# [END Authentication]


# [START API Creation]

Twitter_API = tweepy.API(authentication)

# [END API Creation]


# [START Work]


# Override 'tweepy' built-in method. Add custom logic.
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        # Fetch and print the current Tweet.
        text = status.text.encode('utf-8')

        # Create holder for sentiment analysis.
        status_analysis = textblob.TextBlob(text)

        # Define and print the string analysis.
        status_analysis_str = str(status_analysis.sentiment).encode('utf-8')
        print(status_analysis_str)

        # Append data to record file.
        with open('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataMine-Twitter/raw_tweets_data.txt', 'a') as f:
            f.write(text)
            f.write('\n')


# Define main function.
def main():

    # Create instance of StreamListener.
    stream_listener = StreamListener()

    # Create Stream object.
    twitter_stream = tweepy.Stream(auth= Twitter_API.auth, listener= StreamListener())

    # Initialize DataMine-Twitter stream.
    twitter_stream.filter(track= ['usa'])

main()

# [END Work]
