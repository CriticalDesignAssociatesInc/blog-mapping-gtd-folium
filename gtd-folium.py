# Import the necessary python libraries.
# If they are not installed, run "pip install pandas folium" in your terminal.

import pandas as pd
import folium
from folium.plugins import MarkerCluster

# After downloading the dataset you will need to load it into a Pandas dataframe.
# The "encoding=" argument is important in this case so ensure you are using "ISO-8859-1"
# We also dropping any rows that are missing values, hence the ".dropna(thresh=2)".
# This means we want to drop any rows from the dataframe that have two NaN or Null values.

df = pd.read_csv('globalterrorismdb_0617dist_terms.csv',encoding='ISO-8859-1').dropna(thresh=2)

# Create and instance of the Folium Map using the "cartodpositron" argument for tiles.
# This the base map we will be using for this project. There are others available.
# Reference: https://carto.com/

world_map = folium.Map(tiles="cartodbpositron")

# Since we will be adding marker clusters to the map that show where the terrorism occurred
# we will need to create an instance of this object as well.

marker_cluster = MarkerCluster().add_to(world_map)
# Since our dataset has "latitude" and "longitude" coordinates we will use those to create our markers.
# The for loop below follows this logic. For the entire length of the dataframe overall,
# which gives us our range count. Set the "lat" an "long" variables to the value of each latitude
# and longitude value in the dataframe.
# We set the radius of the marker and the popup_test to show the Country Name and the Terror Group
# These values are also in the dataframe under the columns of "country_text" and "gname".
# Finally we create an iFrame to show the popup text, with the min and max values
# and then we create each marker and add it to the map.
# This may take a long time and the output file will be very large (up to 200MB).

for i in range(len(df)):
    if pd.notna(df.iloc[i]['latitude']):
            lat = df.iloc[i]['latitude']
            long = df.iloc[i]['longitude']
            radius = 5
            popup_text = """Country : {}<br>
                    Terror_Group : {}<br>"""
            popup_text = popup_text.format(df.iloc[i]['country_txt'],df.iloc[i]['gname'])
            iframe = folium.IFrame(popup_text)
            popup = folium.Popup(iframe,min_width=200,max_width=200)
            folium.CircleMarker(location=[lat, long], radius=radius, popup=popup, fill=True).add_to(marker_cluster)

# Finally we save the output of the map with the markers to the file name listed below:

world_map.save(outfile='GTD_Global_Terrorism_Folium.html')
