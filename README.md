# NYC Open Data - Pedestrian Deaths Visualization Dashboard
Data Visualization and Dashboard of NYC Pedestrian and Cyclist Deaths 2012 - 2019

Interactive data visualization for pedestrian and cyclist fatalities in New York City using Bokeh.
As am avid biker and NYC resident, this project was driven by curiousity and search for trends. 

As of 6/4/2020, this is still a work in progress but a basic mvp is presented. 

## Use
Currently, this dashboard only runs locally, i.e., you need to clone this repo and run the code on your machine. 

### Requirements for Reproduction

1. Necessary packages; pandas and bokeh

2. Google maps api key. Get one [here:](https://developers.google.com/maps/documentation/javascript/get-api-key)
Be sure to enable a key for "Maps JavaScript API", there are many different keys and you need the right one. 

3. (Optional) NYC Open Data API app token. 
This is only needed if you want to explore different datasets or change what I have here. Get an API app token [here.](https://opendata.cityofnewyork.us/)

### Load Dashboard

To load the dashboard in your local browser, run the following command in your terminal

`bokeh serve --show nyc_od_peds.py`
