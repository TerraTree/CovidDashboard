import json
import sched
import time
from uk_covid19 import Cov19API
from covid_news_handling import *

'''Both the Covid19API and individual CSV files can be read and put into data form that can be used by the interface.
Can fetch local and national data from the API'''


def parse_csv_data(csv_filename):  # Reads a CSV file and converts it into a list of each line
    fileStrings = []
    fileText = open(csv_filename)  # line ordered by areaCode, areaName, areaType, date,
    for line in fileText:  # First read line is data variable names, second is the most recent day
        # fileStrings.append(line)
        lineData = []
        while line.find(",") != -1:
            lineData.append(line[:line.find(",")])  # Finds the individual data of each value in the line
            line = line[line.find(",") + 1:]  # Removes the previous value from the line
        lineData.append(line[:line.find("/")])
        fileStrings.append(lineData)
    fileText.close()
    return fileStrings


def process_covid_csv_data(covid_csv_data):  # takes the list from the parsed CSV and returns the useful data from it
    cases_7_days = 0
    current_hospital_cases = int(covid_csv_data[1][5])
    cumulative_deaths = int(covid_csv_data[14][4])
    for i in range(3, 10):
        cases = int(covid_csv_data[i][6])
        print("data:" + covid_csv_data[i][6])
        cases_7_days = cases_7_days + cases
    return cases_7_days, current_hospital_cases, cumulative_deaths


def covid_API_request(location="Exeter", location_type="ltla"):
    location_data = [("areaType=" + location_type), ("areaName=" + location)]
    cases_and_deaths = { #dictionary of variables that will be fetched from the API
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
        "hospitalCases": "hospitalCases"
    }
    api = Cov19API(filters=location_data, structure=cases_and_deaths)
    data = api.get_json() #gets the data from the API
    day_7 = 0
    hospital_cases=0
    cum_deaths=0
    for i in range(0, 6):
        day_7 += data["data"][i]["newCasesByPublishDate"] #loop to get the cases for the last 7 days for displaying on the interface
    for day in data["data"]:
        if day["hospitalCases"]!=0 and day["hospitalCases"]!= None and hospital_cases>0:
            hospital_cases=day["hospitalCases"]
        if day["cumDeaths28DaysByDeathDate"]!=0 and day["cumDeaths28DaysByDeathDate"]!= None and cum_deaths>0:
            cum_deaths=day["cumDeaths28DaysByDeathDate"]
        if hospital_cases>0 and cum_deaths>0:
            break
    new_data = {"location": data["data"][0]["areaName"],
                     "7_day_local": day_7,
                     "hospital_cases": hospital_cases,
                     "cum_deaths": cum_deaths}

    return new_data


def schedule_covid_updates(update_interval, update_name):
    # s.enter(20,1,covid_api_request())
    return
