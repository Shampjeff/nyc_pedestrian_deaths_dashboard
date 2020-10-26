import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure, output_notebook, show, gmap
from bokeh.models import CategoricalColorMapper, ColumnDataSource 
from bokeh.models import CheckboxGroup, HoverTool, GMapOptions, Title
from bokeh.models import Legend, CDSView, FactorRange, GroupFilter
from bokeh.layouts import widgetbox, row, column, layout
from bokeh.io import curdoc
from bokeh.transform import factor_cmap
from bokeh.palettes import colorblind


# DATA PREP
# Load data from previous cleaning work
pop_df = pd.read_csv('data/pop_borough', index_col=0)
df = pd.read_csv('data/peds_death_data', index_col=0)

# Drop unneeded columns
df = df.drop(df[(df.borough == 'NOT NYC') | (df.borough.isna() == True)].index)
df = df.drop(['borough_gps', 'location'], axis=1)
# Change data format to datetime
df['total_deaths'] = df.number_of_cyclist_killed+df.number_of_pedestrians_killed
df['month_year'] = pd.to_datetime(df['date']).dt.to_period('M')
df['date'] = pd.to_datetime(df['date'])
# Make a dataframe for deaths by borough and date
data = df.groupby(['month_year', 'borough']).sum() \
    ['total_deaths'].reset_index()

# SMALL AGGREGATE PLOTS
# Line Plot for Totals
# Dropping 2020 for incomplete data
year_df_main = df[(df['year']!= 2012) & (df['year']!= 2020)]
year_df = year_df_main.groupby(['year']).sum()['total_deaths'].reset_index()

source_total = ColumnDataSource(year_df)
y = figure(title = "Total Deaths by Year 2013 - 2019",
           x_axis_label = "Years", 
           y_axis_label = "Number of Deaths", 
           plot_width = 1000,
           plot_height = 300,
           toolbar_location = None,
           tools="")
y.line(x='year', y='total_deaths', 
       source=source_total, 
       color = colorblind["Colorblind"][3][0])
tooltips = [('Deaths', '@total_deaths')]
y.add_tools(HoverTool(tooltips = tooltips))

# Bar plot for Cause of Crash
# More than 5 deaths to be shown
crash_df = df.groupby(['contributing_factor_vehicle_1']) \
            .sum()[['total_deaths']] \
            .reset_index() \
            .sort_values(['total_deaths'], ascending=True)
crash_df = crash_df.loc[crash_df["total_deaths"] >= 5]
y_range = crash_df.contributing_factor_vehicle_1.unique()

# Make data source and configure plot
source_cause = ColumnDataSource(crash_df)
j = figure(y_range=y_range,
           plot_width=500, plot_height=300,
           title="Contributing Factors to Incident",
           toolbar_location=None, tools="") 
j.hbar(y='contributing_factor_vehicle_1',
       right='total_deaths',
       height=0.9, source=source_cause,
       line_color = 'white',
       hover_fill_color='red',
       hover_alpha=1.0,
       hover_line_color='gray')
tooltips = [('Deaths', '@total_deaths')]
j.add_tools(HoverTool(tooltips = tooltips))

# Bar plot for Vehicle type involved
crash_df = df.groupby(['vehicle_type_code1']) \
            .sum()[['total_deaths']] \
            .reset_index() \
            .sort_values(['total_deaths'], ascending=True)
crash_df = crash_df.loc[crash_df["total_deaths"] >= 5]
y_range = crash_df.vehicle_type_code1.unique()
source_vehicle = ColumnDataSource(crash_df)
z = figure(y_range=y_range,
           plot_width=500, plot_height=300,
           title="Vehicle Type in Incident",
           toolbar_location=None, tools="") 
z.hbar(y='vehicle_type_code1',
       right='total_deaths',
       height=0.9, source=source_vehicle,
       line_color = 'white',
       hover_fill_color='red',
       hover_alpha=1.0,
       hover_line_color='gray')
tooltips = [('Deaths', '@total_deaths')]
z.add_tools(HoverTool(tooltips = tooltips))

# BAR OF DEATHS BY BOROUGH AND YEAR
# Grouped bar charts in bokeh are non-trivial

pop_df = pop_df[pop_df.year!=2012]
pop_df = pop_df.groupby(['borough', 'year']) \
                .sum()['population'] \
                .reset_index() \
                .sort_values(['year'], ascending=True)
pop_df['year_mean_pop'] = pop_df.groupby('year').transform('mean')

crash_df = year_df_main.groupby(['borough', 'year']) \
                .sum()[['total_deaths']] \
                .reset_index() \
                .sort_values(['year'], ascending=True)
crash_df['year_mean_deaths'] = crash_df.groupby(["year"]) \
                                        .transform('mean')

# The formatting needed to make a grouped bar chart is challenging

totals = []
pops = []
year_avg_deaths =[]
year_avg_pops = []
group_data = {}
pop_data = {}

boros = crash_df.borough.unique().tolist()
years = crash_df.year.unique().tolist()
year_avg_death = crash_df.year_mean_deaths.tolist()[::5]
year_avg_pop = pop_df.year_mean_pop.tolist()[::5]

for i in range(5):
    year_avg_deaths.extend(year_avg_death)
    year_avg_pops.extend(year_avg_pop)

for i in years: # dict; 'year':[total_1, total_2, ..]
    counts = crash_df[crash_df.year == i] \
                .sort_values('borough').total_deaths.tolist()
    populations = pop_df[pop_df.year == i] \
                .sort_values('borough').population.tolist()
    entry_c = {i:counts}
    entry_p = {i:populations}
    group_data.update(entry_c)
    pop_data.update(entry_p)
    
for i in range(5): # list of ordered seq of totals
    for k, v in group_data.items():
        totals.append(v[i])
for i in range(5): # list of ordered seq of populations
    for k, v in pop_data.items():
        pops.append(v[i])
        
percentage_pop = tuple([(total/pop)*10000 \
                        for pop, total in zip(pops, 
                                              totals)])
avg_percent_pop = tuple([(total/avg_pop)*10000 \
                         for avg_pop, total in zip(year_avg_pops,
                                                   year_avg_deaths)])

totals = tuple(totals) # bokeh needs tuples strings for grouped bars
#list of tuples [ ('Bronx', '2013'), ('brooklyn', '2013')...('Queens', '2018') ]
x = [(str(year), boro) for boro in boros for year in years]

boro_source = ColumnDataSource(data=dict(x=x, 
                                         total=totals,
                                         avg_total=year_avg_deaths,
                                         pop_percent=percentage_pop,
                                         avg_percent=avg_percent_pop))
x_range= FactorRange(*x)
b = figure(x_range=x_range, 
           plot_width=1000, plot_height= 300,
           title="Deaths per Borough by Year",
           toolbar_location=None, tools="")
b.vbar(x='x', top='total',
       width=0.9, source=boro_source,
       line_color = 'white',
       hover_fill_color='red',
       hover_alpha=1.0,
       hover_line_color='gray',
       fill_color=factor_cmap('x',
                              palette=colorblind['Colorblind'][7],
                              factors=boros,
                              start=1, end=2))

b.y_range.start = 0
b.x_range.range_padding = 0.1
b.xaxis.major_label_orientation = 1
b.xgrid.grid_line_color = None

tooltips = [('Deaths', '@total'),
           ('Average Yearly Deaths', '@avg_total')]
b.add_tools(HoverTool(tooltips = tooltips))


b1 = figure(x_range=x_range, 
           plot_width=1000, plot_height= 300,
           title="Percentage Deaths per 10,000",
           toolbar_location=None, tools="")
b1.vbar(x='x', top='pop_percent',
       width=0.9, source=boro_source,
       line_color = 'white',
       hover_fill_color='red',
       hover_alpha=1.0,
       hover_line_color='gray',
       fill_color=factor_cmap('x',
                              palette=colorblind['Colorblind'][7],
                              factors=boros,
                              start=1, end=2))
b1.y_range.start = 0
b1.x_range.range_padding = 0.1
b1.xaxis.major_label_orientation = 1
b1.xgrid.grid_line_color = None

tooltips = [('Percent Deaths', '@pop_percent'),
            ('Yearly Avg', '@avg_percent')]
b1.add_tools(HoverTool(tooltips = tooltips))

layout_1 = column(b,b1)

## ROLLING TOTALS BY BOROUGH

# OBJECTS FOR BOKEH

boro_list = sorted(df.borough.unique().tolist())

checkbox = CheckboxGroup(
            labels=boro_list,
            active=[0,1,2,3,4]
)
idx = pd.date_range(start=df.date.min(), 
                   end=df.date.max())

rolling_df_list = []
for boro in boro_list:
    tmp_df = df[df.borough ==boro] \
        .groupby(['date']).sum()['total_deaths'] \
        .reindex(idx, fill_value=0) \
        .rolling(window=365) \
        .sum() \
        .reset_index() 
    tmp_df['borough'] = boro
    rolling_df_list.append(tmp_df)
    
rolling_df = pd.concat(rolling_df_list, axis=0)
source = ColumnDataSource(rolling_df)

# PLOTTING CALLS
# I would like this to be a line, but that hovertools and 
# interactive use only work for scatter plots in bokeh.
# To update the data based on checkbox interaction, we view a 
# data view called CDSView. These views do not work with line 
# plots. The denisty of the data does give a near-line appearance.

p = figure(title = "One Year Rolling Total 2012 - 2019",
           x_axis_label = "Time", 
           y_axis_label = "Number of Deaths", 
           x_axis_type='datetime', 
           plot_width = 1000, 
           toolbar_location = 'above',
           tools='box_zoom, reset')

p.add_layout(Title(text="Pedestrian and cyclist deaths in each borough",
                   align="left", text_font_style="normal"),"above")

# Filter data based on checkbox selection
for i in range(5):
    view=CDSView(source=source,
                 filters=[GroupFilter(column_name='borough',
                                      group=boro_list[i])])
    p.circle(x='index', y='total_deaths', 
             color=colorblind['Colorblind'][5][i], 
             source=source,
             view=view)
    hover_glyph = p.circle(x='index', y='total_deaths',
                       source=source,
                       size=6, alpha=0,
                       hover_fill_color='red',
                       hover_alpha=0.9)

tooltips = [('Borough', '@borough'),
            ('Total', '@total_deaths'),
            ('Date', "@index{%Y-%m-%d}")]

p.add_tools(HoverTool(tooltips=tooltips,
                       mode='mouse',
                       renderers=[hover_glyph],
                       formatters={'@index':'datetime', }))



# INTERACTIVE CALLBACK
def update_plot(attr, old, new):
    new_boros = [checkbox.labels[i] for i in checkbox.active]
    new_df = rolling_df[rolling_df.borough.isin(new_boros)]
    new_data = {
        'index'  : new_df.loc[:, 'index'],
        'borough'     : new_df.loc[:, 'borough'],
        'total_deaths': new_df.loc[:, 'total_deaths']
    }
    source.data = new_data

checkbox.on_change('active', update_plot)

# MAP OF INCIDENTS

def make_victim_column(row):
    if row.number_of_pedestrians_killed > 1 & \
        row.number_of_cyclist_killed == 0:
        return 'Pedestrian'
    if row.number_of_cyclist_killed > 1 & \
        row.number_of_pedestrians_killed == 0:
        return 'Cyclist'
    else: return 'Both'

map_df = df.dropna(subset=['latitude', 'longitude'])
map_df['victim'] = df.apply(lambda x: make_victim_column(x), axis=1)

map_options = GMapOptions(lat=40.737, 
                          lng=-73.990, 
                          map_type="roadmap", zoom=15)

color_mapper = CategoricalColorMapper(
    factors=["Pedestrian", "Cyclist"],
    palette=[colorblind['Colorblind'][5][1],
    colorblind['Colorblind'][5][0]]
)

hover_map = HoverTool(
    tooltips = [('Date', '@month_year{%Y-%m-%d}'), 
                ('Deaths', '@total_deaths'),
                ('Vehicle Type', '@vehicle_type_code1'),
                ('Cause', '@contributing_factor_vehicle_1')],   
    formatters={'@month_year':'datetime', }
)

g = gmap(google_api_key="AIzaSyBxWE8h20e68cZFV_ppnVPef8w9hUKXf_k", 
         map_options=map_options, 
         title="All Incidents 2012 - 2019", 
         plot_width=1000, 
         toolbar_location = 'above')

map_source = ColumnDataSource(map_df)
g.circle(x='longitude', y='latitude',
         size=10, 
         fill_alpha=1.0, 
         color=dict(field='victim', transform=color_mapper),
         legend='victim',
         source=map_source)
g.legend.location = "top_left"
g.add_tools(hover_map)

# PAGE LAYOUT
row1 = row(p,widgetbox(checkbox))
row2 = row(y)
row3 = row([z,j])
row4 = row(g)

layout = column([row1, row2, row3,layout_1, row4])
curdoc().add_root(layout)



















