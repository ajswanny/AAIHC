import indicoio
import json
import pandas

indicoio.config.api_key = '43c624474f147b8b777a144807e7ca95'




with open('../topic_keywords.json', 'r') as fp:
    set1 = json.load(fp)


series = pandas.Series(set1)

series.drop(labels= "Leyla", inplace= True)

print(series)
