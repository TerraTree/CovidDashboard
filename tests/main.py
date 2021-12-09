"""This module handles the main functionality of Sched and Flask modules, as
well as partial capability of updating the news and data. It listens out for
input from the interface and updates accordingly to the specific input """

import sched
import time
import json
import logging
from flask import request, render_template, Flask
from covid_data_handler import covid_API_request
from covid_news_handling import update_news
from time_conversions import hhmm_to_seconds
from tests import test_covid_data_handler, test_news_data_handling


# import tests.test_covid_data_handler


def add_news_articles():
    """This function changes the articles being displayed on the dashboard
    by adding new articles from the news API"""
    new_news = update_news(covid_terms, old_articles, len(news))
    print("new_news", new_news)
    for article in new_news:
        news.append(article)


def add_data_update():
    """Updates the data that is stored and displayed
    on the dashboard, taking new data from covid19 API"""
    local_data.clear()
    new_loc_data = covid_API_request(local_name, "ltla")
    local_data.update(new_loc_data)
    national_data.clear()
    new_nat_data = covid_API_request(national_name, "nation")
    national_data.update(new_nat_data)


# Initial values to ensure that the code can still work even if config is removed or corrupted
title = "Covid Dashboard"
local_name = ""
covid_terms = ""
national_name = "england"

'''Reads the config.json file and stores it into a dictionary which the
values are then stored into individual variables for use within the code.
If the config file is not found, it raises an exception and the initial values are
used if they weren't already declared in the try statement '''

try:
    config_file = open("config.json")
    data = json.load(config_file)
    national_name = data["national_area_name"]
    local_name = data["local_area_name"]
    covid_terms = data["covid_terms"]
    title = data["dashboard_title"]
    favicon = "/static/images/" + data["favicon"]
    image = "/" + data["favicon"]
except:
    logging.error("Config not found")
    raise Exception

s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
news = []
old_articles = []
update_list = []
# creates an initial dictionary for the local area
local_data = covid_API_request(local_name, "ltla")
# creates an initial dictionary for the national area
national_data = covid_API_request(national_name, "nation")
FORMAT = "%(levelname)s: %(asctime)s %(message)s"
logging.basicConfig(format=FORMAT,filename="log.log")
logging.info("Starting server")


@app.route("/index")
def index():
    """Main function for the website. Runs every time the /index page
    is loaded on the website. Scheduled updates run once the function is
    called next. Request.args.get() functions are called only if it
    receives input and create schedules updates """
    s.run(blocking=False)
    new_array = []
    if request.args.get("notif"):  # triggers if a news notification is removed
        for article in news:
            if article["title"] == request.args.get("notif"):
                # finds the correct article in the list and removes it
                old_articles.append(article)
                news.remove(article)
    elif request.args.get("update_item"):  # triggers if a scheduled update is removed
        for i in range(0, len(update_list)):  # NEED TO DO
            if request.args.get("update_item") == update_list[i]["title"]:
                update_list.remove(update_list[i])
                s.cancel(i)
                break

    elif request.args.get("update"):  # triggers when an update is created with the input forms
        for value in request.args.values():
            # array structure is time, updateName, repeat, isDataUpdate, isNewsUpdate
            new_array.append(value)
        c_time = str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
        delay = hhmm_to_seconds(new_array[0]) - (hhmm_to_seconds(
            c_time) + time.gmtime().tm_sec)  # creates a delay for the scheduled update in seconds
        if "repeat" in new_array:
            pass
            # repeat = True
        if "covid-data" in new_array:
            s.enter(delay, 1, add_data_update)  # schedules a data update
            logging.info("Updating data")
        update_list.append({"title": new_array[1] + " Data",
                            "content": "Data Update: " + new_array[0]})
        if "news" in new_array:
            # create delay
            logging.info("Updating news")
            s.enter(delay, 2, add_news_articles)  # schedules a news update
            update_list.append({"title": new_array[1] + " News",
                                "content": "News Update: " + new_array[0]})

    return render_template("index.html",
                           title=title,
                           favicon=favicon,
                           image=image,
                           news_articles=news,
                           updates=update_list,
                           location=local_data["location"],
                           local_7day_infections=local_data["7_day_local"],
                           nation_location=national_data["location"],
                           hospital_cases='Hospital Cases: ' + str(national_data["hospital_cases"]),
                           deaths_total='Total Deaths: ' + str(national_data["cum_deaths"]),
                           national_7day_infections=national_data["7_day_local"])


if __name__ == "__main__":
    app.run()
