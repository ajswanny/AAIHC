# import requests
# from pprint import pprint
#
#
# subscription_key = "2b3514734bea4e33af85f56f819c2bb0"
# assert subscription_key
# text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
#
#
#
# language_api_url = text_analytics_base_url + "languages"
# key_phrase_api_url = text_analytics_base_url + "keyPhrases"
#
#
# documents = { 'documents': [
#     { 'id': '1', 'text': 'Apple intern reportedly leaked iPhone source code' },
# ]}
#
#
#
# headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
# response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
# languages = response.json()
# pprint(languages)

