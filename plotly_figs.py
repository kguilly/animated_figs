import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from metpy.plots import USSTATES
from matplotlib.cm import ScalarMappable
import cartopy.crs as ccrs

import plotly.figure_factory as ff

from urllib.request import urlopen
import json
import plotly.express as px
import plotly.io as pio


# retrieve the weather data for the whole U.S.
def retrieve_us_data(month, day):
  file_template = "2022-{}.csv"
  targeted_month = file_template.format(month)

  all_data = []
  # iterate over the states
  for state_dir in os.listdir(directory):
      state_path = os.path.join(directory, state_dir)

       # iteratore over the files in the dir
      for file in os.listdir(state_path):
        if file.endswith(targeted_month):
          # full path to file
          file_path = os.path.join(state_path, file)
          df = pd.read_csv(file_path)

          # only consifer the monthly data for visualization
          df = df[df["Daily/Monthly"] == "Daily"]
          df = df[df["Day"] == day]
          # hanlde the fips code
          df["FIPS Code"] = df["FIPS Code"].astype(str).str.zfill(5)
          all_data.append(df)

  # concatenate all dfs into a single one
  us_data = pd.concat(all_data)
  return us_data

def save_png(us_data, counties, month, day):
  fig = px.choropleth(us_data, geojson=counties, locations='FIPS Code', color='Avg Temperature (K)',
                          color_continuous_scale="Jet",
                          range_color=(260, 300),
                          scope="usa",
                          labels={'Avg Temperature (K)':'Temperature (K)'}
                        )
  title = "Temperature: 2022-" + str(month) + "-" + str(day)

  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    coloraxis_colorbar=dict(lenmode='fraction', len=0.75),
                    title=title)
  pio.write_image(fig, f"plotly_figs/{day:003}.png")

# loop through the first 14 days of a month, plot the daily data for all 14 days
directory = "/media/kaleb/extraSpace/crop/fudong_figs/2022"
month = "01"
days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
     counties = json.load(response)

for day in days:
   us_data = retrieve_us_data(month, day)
   
   save_png(us_data, counties, month, day)

# save as a gif
os.system("convert -delay 30 plotly_figs/*.png plotly_test.gif")
   