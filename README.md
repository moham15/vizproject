# vizproject
This readme file is about a web app that allows exploration of earthquake data. It uses the Streamlit library to create a user interface and the Pandas library to preprocess and clean the data. The app allows users to explore the data by displaying a density map, a correlation between depth and magnitude, a line chart of the entire period, a bubble scatter plot, and a histogram of the events. It also allows users to filter the data by date and place.

The script then defines a "home" function that creates the main page for the web app. This page contains several plots and charts that visualize the earthquake data, such as a density map, a scatterplot showing the relationship between depth and magnitude, and a bubble chart that shows the magnitude of earthquakes over time. The page also includes a summary of the data and several other statistics.

1) Install the required libraries. The script uses the Streamlit and Pandas libraries, so you will need to install them  in order to run the script:

2) To run this streamlit application, one needs to run the output of the code through the python or anaconda command prompt

3) The dashboard is shown by typing 'streamlit run "path where the script is located" ending with \app.py' in the command prompt;
such as: C:\Users\stefan\Desktop\Visualization\app.py

4) There are 3 main controls: dates, dropdown (locations), and page navigation. Please note is "show all places" is selected, the dropdown option will not be visible

5) Due to an unresolved bug, the map updates slowly when trying to showcase all dots on the scatter map for the magnitudes on the all map page. This is currently being worked on

