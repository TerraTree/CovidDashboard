"""Creates a list of news articles for the dashboard, using the News API"""

import requests


def news_API_request(covid_terms="Covid COVID-19 coronavirus", news_api_key="") -> list:
    """Uses the newsAPI to fetch a list of dictionaries
    from their website that will be displayed onto the interface and
    can add new news articles that are not currently in the list """
    url = (
            "https://newsapi.org/v2/everything?q=" + covid_terms +
            "&from=2021-11-08&apiKey=" + news_api_key)
    # try:
    response = requests.get(url)
    return response.json()["articles"]
    # except:
    #    return None


def update_news(terms: str, old_articles: list, current_len=0, news_api_key="") -> list:
    """Increases the number of articles displayed up to the
    limit given by reading from the list of new articles from
    the news API """
    new_array = []
    new_articles = news_API_request(terms, news_api_key)
    index = current_len
    for article in new_articles:
        reduced_article = {"title": article["title"], "content": article["description"]}
        if index == 10 - current_len:  # Limit of articles on the page
            break
        if reduced_article in old_articles:
            pass
        else:
            new_array.append(reduced_article)
            index += 1
    return new_array
