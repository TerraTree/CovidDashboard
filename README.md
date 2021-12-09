# Covid Dashboard

This is a Covid Dashboard for viewing Covid-19 data for local and national areas and news related to Covid-19.

The source code is also available on [Github](https://github.com/TerraTree/CovidDashboard)

# Dependencies

Python 3.10+ is required to use this, but earlier versions may work.

Additional modules not preinstalled with Python will be required to run this.

 [Covid-19 API](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/)

    pip install uk-covid19

 [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)

    pip install Flask

[newsAPI](https://newsapi.org/): Need to create a free account and add your API key to the config file

## Getting Started
Before running the code, go to the config.json file and add your API key to the config. There, you can also change:

 - Local location
 - National location (e.g England)
 - Specific Covid related terms for searching for news
 - Name of dashboard

To run the code, run the Main.py file.
On a web browser, go to the address http://127.0.0.1:5000/index.
From there, you can control the dashboard using the interface, with control over when to set updates.
Updates can be removed by removing them from the left side of the interface.
News articles can be removed, after which they will not appear

## Documentation

Documentation can be found in the docs/build/index.html file, listing the modules used within the code

## Details

Developed by William Liversidge



