import tests.test_covid_data_handler
from covid_data_handler import *
from covid_news_handling import *
from flask import *
import sched
import time
import json
from time_conversions import *
from tests import test_covid_data_handler
from tests import test_news_data_handling


def add_news_articles(): #adds the news articles from the news API to the news list
    new_news = update_news(covid_terms, old_articles, len(news), news_api_key)
    print("new_news", new_news)
    for article in new_news:
        news.append(article)


def add_data_update(): #Clears and then adds the updated data back to the dictionaries for both local and national data
    local_data.clear()
    new_loc_data = covid_API_request(local_name, "ltla")
    local_data.update(new_loc_data)
    national_data.clear()
    new_nat_data = covid_API_request(national_name, "nation")
    national_data.update(new_nat_data)


data_tests = tests.test_covid_data_handler
data_tests.test_covid_API_request()
data_tests.test_parse_csv_data()
data_tests.test_schedule_covid_updates()
data_tests.test_process_covid_csv_data()

news_tests = tests.test_news_data_handling
#news_tests.test_news_API_request()
# news_tests.test_update_news()

# Initial values to ensure that the code can still work even if config is removed or corrupted
title = "Covid Dashboard"
local_name = ""
covid_terms = ""
national_name = "england"
news_api_key = ""

'''Reads the config.json file and stores it into a dictionary which the values are then stored into individual 
variables for use within the code. If the config file is not found, it raises an exception and the initial values are 
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
    news_api_key = data["news_api_key"]
except:
    raise Exception

s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
news = []
old_articles = []
update_list = []
local_data = covid_API_request(local_name, "ltla")  # creates an initial dictionary for the local area
national_data = covid_API_request(national_name, "nation")  # creates an initial dictionary for the national area

'''Main function for the website. Runs every time the /index page is loaded on the website. Scheduled updates run 
once the function is called next. Request.args.get() functions are called only if it receives input and create 
schedules updates '''


@app.route("/index")
def alarm():
    s.run(blocking=False)
    newArray = []
    if request.args.get("notif"):  # triggers if a news notification is removed
        for article in news:
            if article["title"] == request.args.getlist("notif")[0]: #finds the correct article in the list and removes it
                old_articles.append(article)
                news.remove(article)
    elif request.args.get("update_item"): # triggers if a scheduled update is removed
        for i in range(0, len(update_list)):  # NEED TO DO
            s.cancel()
    elif request.args.get("update"): #triggers when an update is created with the input forms
        for value in request.args.values():
            newArray.append(value)  # array structure is time, updateName, repeat, isDataUpdate, isNewsUpdate
        c_time = str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
        delay = hhmm_to_seconds(newArray[0]) - (hhmm_to_seconds(c_time) + time.gmtime().tm_sec) #creates a delay for the scheduled update in seconds
        if "repeat" in newArray:
            repeat = True
        if "covid-data" in newArray:
            s.enter(delay, 1, add_data_update) #schedules a data update
            update_list.append({"title": newArray[1] + " Data", "content": "Data Update: " + newArray[0]})
        if "news" in newArray:
            # create delay
            s.enter(delay, 2, add_news_articles) #schedules a news update
            update_list.append({"title": newArray[1] + " News", "content": "News Update: " + newArray[0]})

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
