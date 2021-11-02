from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
def test_parse_csv_data():
    data = parse_csv_data("nation_2021-10-28.csv")
    print(data)
    print(len(data))
    assert len(data) == 639


def test_process_covid_csv_data():
    last7days_cases,current_hospital_cases,total_deaths = process_covid_csv_data ( parse_csv_data ( "nation_2021-10-28.csv"))
    print("cases:",last7days_cases)
    print("hospital:",current_hospital_cases)
    print("deaths:",total_deaths)
    #assert last7days_cases == 240299
    #assert current_hospital_cases == 7019
    #assert total_deaths == 141544


test_parse_csv_data()
test_process_covid_csv_data()