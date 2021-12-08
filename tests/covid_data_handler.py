"""Both the Covid19API and individual CSV files can be
read and put into data form that can be used by the interface.
Can fetch local and national data from the API"""

from uk_covid19 import Cov19API


def parse_csv_data(csv_filename: str) -> list:
    """Reads a CSV file and converts it into a list of each line"""
    file_strings = []
    # line ordered by areaCode, areaName, areaType, date
    file_text = open(csv_filename)
    # First read line is data variable names, second is the most recent day
    for line in file_text:
        line_data = []
        while line.find(",") != -1:
            # Finds the individual data of each value in the line
            line_data.append(line[:line.find(",")])
            # Removes the previous value from the line
            line = line[line.find(",") + 1:]
        line_data.append(line[:line.find("/")])
        file_strings.append(line_data)
    file_text.close()
    return file_strings


def process_covid_csv_data(covid_csv_data: list):
    """Reads a list of lines from the CSV file
    and takes the useful variables usable in the dashboard"""
    cases_7_days = 0
    covid_csv_data.remove(covid_csv_data[0])
    for days in covid_csv_data:
        if days[5] == "":
            pass
        elif int(days[5]) != 0 and days[5] is not None:
            current_hospital_cases = int(days[5])
            break
    for days in covid_csv_data:
        if days[4] == "":
            pass
        elif int(days[4]) != 0 and days[4] is not None:
            cumulative_deaths = int(days[4])
            break
    for i in range(2, 9):
        cases = int(covid_csv_data[i][6])
        print("data:" + covid_csv_data[i][6])
        cases_7_days = cases_7_days + cases
    return cases_7_days, current_hospital_cases, cumulative_deaths


def covid_API_request(location="Exeter", location_type="ltla") -> dict:
    """Requests a json dictionary from the uk_covid19 API,
    using parameters to find certain locations in England"""
    location_data = [("areaType=" + location_type), ("areaName=" + location)]
    cases_and_deaths = {  # dictionary of variables that will be fetched from the API
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
    data = api.get_json()  # gets the data from the API
    day_7 = 0
    hospital_cases = 0
    cum_deaths = 0
    for i in range(0, 6):
        # loop to get the cases for the last 7 days for displaying on the interface
        day_7 += data["data"][i]["newCasesByPublishDate"]
    for day in data["data"]:
        if day["hospitalCases"] != 0 and day["hospitalCases"] is not None and hospital_cases > 0:
            hospital_cases = day["hospitalCases"]
        if day["cumDeaths28DaysByDeathDate"] != 0 \
                and day["cumDeaths28DaysByDeathDate"] is not None \
                and cum_deaths > 0:
            cum_deaths = day["cumDeaths28DaysByDeathDate"]
        if hospital_cases > 0 and cum_deaths > 0:
            break
    new_data = {"location": data["data"][0]["areaName"],
                "7_day_local": day_7,
                "hospital_cases": hospital_cases,
                "cum_deaths": cum_deaths}

    return new_data


def schedule_covid_updates(update_interval, update_name):
    """Schedules a data update"""
    # s.enter(20,1,covid_api_request())
    return
