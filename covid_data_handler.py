def parse_csv_data(csv_filename):
    fileStrings=[]
    fileText = open(csv_filename) #line ordered by areaCode, areaName, areaType, date,
    for line in fileText: #First read line is data variable names, second is the most recent day
        lineData = []
        while line.find(",") != -1:
            lineData.append(line[:line.find(",")]) #Finds the individual data of each value in the line
            line = line[line.find(",")+1:] #Removes the previous value from the line
        lineData.append(line[:line.find("/")])
        fileStrings.append(lineData)
    fileText.close()
    return fileStrings

def process_covid_csv_data(covid_csv_data):
    cases_7_days = 0
    current_hospital_cases = covid_csv_data[2][5]
    cumulative_deaths = covid_csv_data[14][4]
    for i in range(3,7):
        cases = int(covid_csv_data[i][6])
        print("data:"+covid_csv_data[i][6])
        cases_7_days = cases_7_days+ cases
    return cases_7_days,current_hospital_cases,cumulative_deaths
