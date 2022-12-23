
#______________________Importing the required Libraries________________________
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#_____________________________SETUP____________________________________________

st.set_page_config(layout="wide")
#read csv file preprocessing data cleaning
#This will cache the dataframe in memory, so it doesn't have to be read from the CSV file every time the app is run.
df = st.cache(pd.read_csv)("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv")

#renaming the time column to date
df.rename(columns={'time': 'date'}, inplace=True)
#dropping unnecessary columns
df = df.drop(columns=["magType", "nst", "dmin", "rms", "net", "id", "horizontalError",
                      "depthError", "magError", "magNst", "locationSource", "magSource", "gap"])

# filtering the place column so only the place shows in the field or in this case the last word in the column
df['place'] = df['place'].str.replace(r'^[^,]*,\s*', '', regex=True)
# sorting the places in alphabetic order
df = df.sort_values('place')
    

##PAGE TITLE
# Add a title and intro text
st.title('Earthquake Data Explorer')
st.text('This is a web app to allow exploration of Earthquake Data')

#This is a dictionary mapping continents to lists of countries or regions associated with those continents. It includes an entry for each continent and lists the countries or regions that 
#belong to that continent. The dictionary also includes an entry for Antarctica with an empty list.
continent_dict = {
    'Africa': ['Algeria', 'Gabon', 'Morocco', 'Mozambique', 'South Africa', 'Tanzania', 'Tunisia', 'Yemen'],
    'Antarctica': [],
    'Asia': ['Afghanistan', 'Afghanistan-Tajikistan border region', 'China', 'Cyprus', 'Eastern Mongolia', 'India', 'Indonesia', 'Iran', 'Japan', 'Kyrgyzstan', 'Kyrgyzstan-Tajikistan border region', 'Mongolia', 'Myanmar', 'Pakistan', 'Papua New Guinea', 'Russia', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor Leste', 'Turkey', 'Turkmenistan', 'Western Turkey'],
    'Australia': ['Australia', 'Macquarie Island region', 'Western Australia'],
    'Europe': ['Albania', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'France', 'Greece', 'Italy', 'Kosovo', 'Malta', 'Montenegro', 'Portugal', 'Romania', 'Serbia', 'Slovenia', 'Spain'],
    'North America': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'British Columbia', 'California', 'Canada', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Ontario', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'],
    'South America': ['Argentina', 'Bolivia', 'Chile', 'Colombia', 'Ecuador', 'El Salvador', 'French Guiana', 'Guyana', 'Panama', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'],
    'Oceania': ['American Samoa', 'Antigua and Barbuda', 'Australia', 'Fiji', 'French Polynesia', 'Guam', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tokelau', 'Tonga', 'Tuvalu', 'Vanuatu', 'Wallis and Futuna'],
    'Polar regions': ['Antarctica', 'Arctic Ocean', 'Greenland', 'Svalbard and Jan Mayen']
}
#creates a list of continent names by extracting the keys of the continent_dict dictionary.
continent_names = list(continent_dict.keys())
#adds a caption to the sidebar of a streamlit app explaining the purpose of the dashboard and where the data is coming from.
st.sidebar.caption("This dashboard contains information for every recent earhtquake registered in USGS .The data is collected from the  website: https://earthquake.usgs.gov/earthquakes/")
# creates a multi-select widget in the sidebar of the streamlit app that allows the user to select one or more continents from a list of options. The selected continents are stored in a variable called selected_continents.
selected_continents = st.sidebar.multiselect("Please select a continent:", options=continent_names, default=continent_names)
#creates an empty list called selected_countries that will be used to store the selected countries.
selected_countries = []
#The for loop will continue to iterate through each continent in the selected_continents list and add the corresponding countries to the selected_countries list until all continents have been processed.
for continent in selected_continents:
    selected_countries += continent_dict[continent]

#selecting rows from the dataframe df where the value in the place column is contained in the list selected_countries. The resulting dataframe will only contain rows where the place value is in selected_countries.
df = df[df['place'].isin(selected_countries)]

#_____________________________HOME PAGE________________________________________

def home():
      
      
    # Display the data table using the st.dataframe function
    st.header('Overview')

    data_table()
        
    # Display the density map with only the selected earthquake using the st.plotly_chart function
    st.header('Density Map')
    st.plotly_chart(printDensityMap(df,selected_continents), use_container_width=True)    
    st.write('Please note that z value is magnitude')
    # dividing content in two columns
    col1, col2 = st.columns(2)

    with col1:
        # plot 1
        # title
        st.header("Depth vs Magnitude")
        st.text("This is the correlation between depth and magnitude")
        st.plotly_chart(displayplot(df,selected_continents))

    with col2:
        st.header("Magnitude line chart")
        st.text("This shows the line chart for the entire period")
        st.line_chart(printMgLineChart(df,selected_continents))

    # title
    st.header("Earthquakes bubble chart")
    st.text("Please note when choosing the dates, it only outputs when there is an earthquake with a magnitude above 3 ")
    # bubble scatter plot
    st.plotly_chart(printBubbleScatter(df,selected_continents), use_container_width=True)
    

#_____________________________DATA SUMMARY PAGE________________________________

# function  summary/stats
def data_summary(df,selected_continents):
    
	# title
    st.header("Number of events")
    st.plotly_chart(histEvents(df,selected_continents))

    #making two columns
    col1, col2 = st.columns(2)
    with col1:
        st.header("Repartitions")
        st.plotly_chart(repartition(df,selected_continents))
    with col2:
        st.header("Proportions")
        st.text("This is the proportions of differnet events")
        st.plotly_chart(pie(df,selected_continents))

#ALL THE FUNCTIONS
def data_table():
    st.dataframe(df)
   
def displayplot(df,selected_continents):
    fig = px.scatter(df, x='depth', y='mag')
    return fig

#This function generates a density map plot of earthquake magnitudes in a given dataframe, filtered to only include rows with magnitude >= 1. 
# It uses the px.density_mapbox function from the Plotly library and returns the resulting figure object.
def printDensityMap(df,selected_continents):
    df = df.loc[df['mag'] >= 1 ]
    lon = df['longitude'].tolist()
    lat = df['latitude'].tolist()
    
    fig = px.density_mapbox(lat=lat, lon=lon,
                            z=df["mag"], radius=15, mapbox_style="open-street-map", zoom=2)
    fig.update_layout(title="Magnitude",margin={"r": 0, "t": 0, "l": 0, "b": 0})

    
    return fig


# function for bubble scatter plot
def printBubbleScatter(df,selected_continents):
    fig = px.scatter(df[df['mag'] >= 3], x='date', y='mag', size='mag', color='mag')
    return fig

# function for histogram
def histEvents(df,selected_continents):
    fig = px.histogram(df, 'date', color="type")
    return fig

# Function for linechart
def printMgLineChart(df,selected_continents):
    data = df["mag"]
    return data
#The function repartition filters a dataframe to include only rows where the 'type' column is 'earthquake', and creates a histogram plot using the 'mag' column and plotly express. 
# It returns the plot with a title of 'Repartition of magnitude earthquakes
def repartition(df,selected_continents):
    earthquakes_rep = df.loc[df['type'] == 'earthquake',:]
    fig = px.histogram(earthquakes_rep, x = 'mag', nbins=50,title='Repartition of magnitude earthquakes')
    return fig

#pie diagram showing different types of events
def pie(df,selected_continents):
    piefig = px.pie(data_frame=df,
       names='type',
       title='Proportions of events')
    return piefig


#__________________________________SIDEBAR_____________________________________

#filtering date and time
df['date'] = pd.to_datetime(df['date'])
df['date_only'] = df['date'].dt.date
df['time_only'] = df['date'].dt.strftime('%H:%M:%S')

#The first line converts the date column in the dataframe to a date format. 
df['date_only'] = pd.to_datetime(df['date_only']).dt.date

min_date = df['date_only'].min()
max_date = df['date_only'].max()


#The next two lines create a start and end date input in the sidebar.
st.sidebar.text("Please choose the start date")
#start_dt = st.sidebar.date_input('Start date', value=df['date_only'].min())
start_dt = st.sidebar.date_input('Start date', value=min_date, min_value=min_date, max_value=max_date)


st.sidebar.text("Please choose the\n start end date")
#end_dt = st.sidebar.date_input('End date', value=df['date_only'].max())
end_dt = st.sidebar.date_input('End date', value=max_date, min_value=min_date, max_value=max_date)

#The if statement checks if the start date is less than or equal to the end date. If it is, 
#the dataframe is filtered to only include dates between the start and end date.     
if start_dt <= end_dt:
   df = df[df['date_only'] >= start_dt]
   df = df[df['date_only'] <= end_dt]
else:
    st.error('Start date must be <= End date')

# Sidebar navigation
st.sidebar.header('Navigation')
options = st.sidebar.radio('Select what you want to display:', [
    'Home', 'Data Summary'])

# Navigation options
if options == 'Home':
    home()
elif options == 'Data Summary':
    data_summary(df,selected_continents)



