import uvicorn
from fastapi import FastAPI
import requests
from pydantic import BaseModel
import json
import time


app = FastAPI()


class NewsArticle(BaseModel):
    
    keywords: str
    sources: str
    #url: str

@app.post('/getSentimentFromKeywords')
async def get_newsarticles(news: NewsArticle):
    
    x={"keywords":news.keywords,"sources":news.sources}
    response = requests.post('http://localhost:8008/get_news_urls_from_keywords_googlenewspage', data = json.dumps(x))
    #response = requests.post('http://20.244.72.50:8008/get_news_url_from_keywords', data = json.dumps(x))
    response = response.text
    t = json.loads(response)
    final=[]
    
    for i in t['urls'][0:1]:

        try:
            ## following is the code to extract the title and the body of the news from the above got url
            x1 = {"url": i}
            #response1 = requests.post('http://localhost:8009/getarticle', data = json.dumps(x1))
            response1 = requests.post('http://20.204.224.207:8009/getBodyContentFromUrl', data = json.dumps(x1))
            response1 = response1.text
            news_body = json.loads(response1)
            news_title = news_body['title'] ###### should be returned as the final results
            news_body = news_body['body'] 

            ## following code is to extract the keywords from the text
            x3 = {"text":news_body}
            #response3 = requests.post('http://nxt_nlp_sentiment_keyword_service:8007/getkeyphrases', data = json.dumps(x3))
            response3 = requests.post('http://20.219.230.210:8010/getKeyWordsFromText', data = json.dumps(x3))
            response3 = response3.text
            keywords = json.loads(response3)
            keywords = keywords["keywords"]




            ## the following code is to summarize the above news body to 100 words summary
            x2 = {"text":news_body,"summary_words":100}
            #response2 = requests.post('http://nxt_nlp_text_summarization_service:8005/getSummaryByWords', data = json.dumps(x2))
            response2 = requests.post('http://20.244.56.36:8005/getSummaryByWords', data = json.dumps(x2))
            response2 = response2.text
            summarized_text = json.loads(response2)
            summarized_text = summarized_text["Summary"]

            ## the following code is to get the sentiment and the sentiment score
            x4 = {"text":summarized_text}
            print(f"The input text for sentiment is {x4}")
            #response4 = requests.post('http://nxt_nlp_sentiment_keyword_service:8007/getsentiment', data = json.dumps(x4))
            response4 = requests.post('http://4.224.104.177:8007/getSentimentFromText', data = json.dumps(x4))
            response4 = response4.text
            sentiment = json.loads(response4)

            final.append({"search keywords":news.keywords,
                        "title":news_title,
                        "full_article":news_body,
                        "keywords":keywords,
                        "summary":summarized_text,
                        "sentiment":sentiment["label"],
                        "sentiment_score":sentiment['score']})
        except Exception as e:
            return e



    
        



    return final
    


    



"""

@app.post('/keyword_sentiment_post_text')
def get_keyword_sentiment(keyword_sentiment_post:Sentiment):
    t = {"text":keyword_sentiment_post.sentimenttext}
    response = requests.post('http://second:8080/getsentiment', data = json.dumps(t))
    response = response.text
    return (json.loads(response))

"""


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)