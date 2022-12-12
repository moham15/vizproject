# Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


st.set_page_config(layout="wide")


#read csv file preprocessing data cleaning
df = pd.read_csv(
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv")

df.rename(columns={'time': 'date'}, inplace=True)

df = df.drop(columns=["magType", "nst", "dmin", "rms", "net", "id", "horizontalError",
                      "depthError", "magError", "magNst", "locationSource", "magSource", "gap"])

# filtering the place column so only the place shows in the field or in this case the last word in the column
df['place'] = df['place'].str.replace(r'^[^,]*,\s*', '')
# sorting the places in alphabetic order
df = df.sort_values('place')


          
##PAGE TITLE
# Add a title and intro text
st.title('Earthquake Data Explorer')
st.text('This is a web app to allow exploration of Earthquake Data')


def home():
    st.header('overview')
    data_header()

    # density map
    st.header('Density Map')
    st.plotly_chart(printDensityMap(), use_container_width=True)
    # dividing content in two columns
    col1, col2 = st.columns(2)

    with col1:
        # plot 1
        # title
        st.header("Depth vs Magnitude")
        st.text("This is the correlation between depth and magnitude")
        st.plotly_chart(displayplot())

    with col2:
        st.header("Magnitude line chart")
        st.text("This shows the line chart for the entire period")
        st.line_chart(printMgLineChart())

    # title
    st.header("Earthquakes bubble chart")
    st.text("Please note when choosing the dates, it only outputs when there is an earthquake with a magnitude above 3 ")
    # bubble scatter plot
    st.plotly_chart(printBubbleScatter(df), use_container_width=True)
 
    
    

# function for dataframe summary/stats
def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df.describe())
	# title
    st.header("Number of events")
    st.plotly_chart(histEvents())

    col1, col2 = st.columns(2)
    with col1:
        st.header("Repartitions")
        st.plotly_chart(repartition())
    with col2:
        st.header("Proportions")
        st.text("This is the proportions of differnet events")
        st.plotly_chart(pie())



#ALL THE FUNCTIONS
def data_header():
    st.write(df.head())
   
def displayplot():
    fig = px.scatter(df, x='depth', y='mag')
    return fig


# function for density map
def printDensityMap():
    fig = px.density_mapbox(lat=df["latitude"], lon=df["longitude"],
                            z=df["mag"], radius=10, mapbox_style="open-street-map", zoom=2)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# function for bubble scatter plot
def printBubbleScatter(df):
    fig = px.scatter(df[df['mag'] >= 3], x='date', y='mag', size='mag', color='mag')
    return fig

# function for histogram
def histEvents():
    fig = px.histogram(df, 'date', color="type")
    return fig

# Function for linechart
def printMgLineChart():
    data = df["mag"]
    return data

def repartition():
    earthquakes_rep = df.loc[df['type'] == 'earthquake',:]
    fig = px.histogram(earthquakes_rep, x = 'mag', nbins=50,title='Repartition of magnitude earthquakes')
    return fig

def pie():
    piefig = px.pie(data_frame=df,
       names='type',
       title='Proportions of events')
    return piefig


# function for magnitude map
def magMap():
    earthquakes = df.loc[df['type'] == 'earthquake', :]
    fig = px.scatter_mapbox(earthquakes, lat="latitude", lon="longitude", color="mag",
                            mapbox_style="open-street-map", zoom=2, color_continuous_scale='Reds')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# function to display all maps
def displayAllMaps():
    st.header('Map')
    magPlot = magMap()
    st.plotly_chart(magPlot, use_container_width=True)

    # densitymap
    st.header('Density Map')
    mapPlot = printDensityMap()
    st.plotly_chart(mapPlot, use_container_width=True)


#### SIDEBAR

#filtering date and time
df['date'] = pd.to_datetime(df['date'])
df['date_only'] = df['date'].dt.date
df['time_only'] = df['date'].dt.strftime('%H:%M:%S')

#The first line converts the date column in the dataframe to a date format. 
df['date_only'] = pd.to_datetime(df['date_only']).dt.date


#The next two lines create a start and end date input in the sidebar.
st.sidebar.text("Please choose the start date")
start_dt = st.sidebar.date_input('Start date', value=df['date_only'].min())

st.sidebar.text("Please choose the end date")
end_dt = st.sidebar.date_input('End date', value=df['date_only'].max())

#The if statement checks if the start date is less than or equal to the end date. If it is, 
#the dataframe is filtered to only include dates between the start and end date.     
if start_dt <= end_dt:
   df = df[df['date_only'] >= start_dt]
   df = df[df['date_only'] <= end_dt]
else:
    st.error('Start date must be <= End date')

# Add a checkbox to the sidebar
st.sidebar.text("If you want to see all places\nplease check the box")
all_places = st.sidebar.checkbox('Show all places')
#dropdown
if all_places:
    df = df
else:
    places_filter=st.sidebar.selectbox("Select the places", pd.unique(df['place']))
    df = df[df['place']==places_filter]


# Sidebar navigation
st.sidebar.header('Navigation')
options = st.sidebar.radio('Select what you want to display:', [
    'Home', 'Data Summary',  'Map Plots'])

# Navigation options
if options == 'Home':
    home()
elif options == 'Data Summary':
    data_summary()
elif options == 'Map Plots':
    displayAllMaps()


