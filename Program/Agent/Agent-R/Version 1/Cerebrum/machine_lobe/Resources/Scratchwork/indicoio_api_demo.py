import indicoio

indicoio.config.api_key = '43c624474f147b8b777a144807e7ca95'

# single example
# print(indicoio.sentiment("I wish I had learned writing code!"))

# batch example
# indicoio.sentiment([
#     "I love writing code!",
#     "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
# ])


x = indicoio.summarization("https://www.cnn.com/2017/10/20/us/puerto-rico-one-month-santiago/index.html")


print(x)
