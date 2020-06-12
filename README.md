# NYC Open Data - Pedestrian Deaths Visualization Dashboard
Data Visualization and Dashboard of NYC Pedestrian and Cyclist Deaths 2012 - 2019

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Shampjeff/nyc_pedestrian_deaths_dashboard/master?urlpath=/proxy/5006/bokeh-app)


Interactive data visualization for pedestrian and cyclist fatalities in New York City using Bokeh.
As an avid biker and NYC resident, this project was driven by curiousity and search for trends. 

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


## Example

If you would like to the and use (some!) of the plots and interactive features they are viewable in the file
`Pedestrian_deaths_dashboard_dev.ipynb` 

## Data ETL

The data ETL file is contained in the file, `Pedestrian Deaths Data Load and Cleaning.ipynb`. This file details how unassigned borough were determined, how vehicle types and contributing factors to the incidents were grouped. 

# Running a bokeh server with Binder

To visualize the data publicly, we need another service to load and run the bokeh app, this can be done with Binder. I found a template for doing this from [this cool repo](https://github.com/binder-examples/bokeh)

The `bokeh-app` directory and the associated files; `bokehserverextension.py`,`environment.yml`, `postBuild` are from the above repo and enable this dashboard to run. Please see the file `LICENSE` for usage details. 


