import requests
import sched

'''Uses the newsAPI to fetch a list of dictionaries from their website that will be displayed onto the interface and 
can add new news articles that are not currently in the list '''


def news_API_request(covid_terms="Covid COVID-19 coronavirus", news_api_key=""):
    url = (
            "https://newsapi.org/v2/everything?q=" + covid_terms + "&from=2021-11-08&apiKey=" + news_api_key)
    #try:
    response = requests.get(url)
    return response.json()["articles"]
    #except:
    #    return None


def update_news(terms, old_articles, current_len=0, news_api_key=""):
    new_array = []
    new_articles = news_API_request(terms, news_api_key)
    index = current_len
    for article in new_articles:
        reduced_article = {"title": article["title"], "content": article["description"]}
        if index == 10 - current_len:
            break
        if reduced_article in old_articles:
            pass
        else:
            new_array.append(reduced_article)
            # new_array.append(article)
            index += 1
    return new_array
