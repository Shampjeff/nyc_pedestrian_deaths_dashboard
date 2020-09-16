# NYC Open Data - Pedestrian Deaths Visualization Dashboard
Data Visualization and Dashboard of NYC Pedestrian and Cyclist Deaths 2012 - 2019

![Heroku](https://pyheroku-badge.herokuapp.com/?app=<main-bokeh-shamp>&style=flat)


Interactive data visualization for pedestrian and cyclist fatalities in New York City using Bokeh.
As an avid biker and NYC resident, this project was driven by curiousity and search for trends. 


## Use
Currently, this dashboard can run locally, or can be used via the binder link to load it in any browser.  

### Requirements for Reproduction

If you want to run this locally, complete the following steps:

1. Necessary packages; pandas and bokeh

2. Google maps api key. Get one [here:](https://developers.google.com/maps/documentation/javascript/get-api-key)
Be sure to enable a key for "Maps JavaScript API", there are many different keys and you need the right one. 

3. (Optional) NYC Open Data API app token. 
This is only needed if you want to explore different datasets or change what I have here. Get an API app token [here.](https://opendata.cityofnewyork.us/)

### Load Dashboard Locally

To load the dashboard in your local browser, run the following command in your terminal

`bokeh serve --show bokeh-app/main.py`


## Example

If you would like to the and use (some!) of the plots and interactive features they are viewable in the file
`Pedestrian_deaths_dashboard_dev.ipynb` 

## Data ETL

The data ETL file is contained in the file, `Pedestrian Deaths Data Load and Cleaning.ipynb`. This file details how unassigned borough were determined, how vehicle types and contributing factors to the incidents were grouped. 

# Running a bokeh server with Heroku

To visualize the data publicly, we need another service to load and run the bokeh app, this can be done with Heroku. 



