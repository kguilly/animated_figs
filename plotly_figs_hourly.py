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

from datetime import datetime

# retrieve the weather data for the whole U.S.
def retrieve_us_data(month, day, hour):
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
          df = pd.read_csv(file_path, index_col=False)

          # only consifer the monthly data for visualization
          df = df[df["Daily/Monthly"] == "Daily"]
          df = df[df["Day"].isin(day)]
          df = df[df['Hour'].isin(hour)]
          # hanlde the fips code
          df["FIPS Code"] = df["FIPS Code"].astype(str).str.zfill(5)
          all_data.append(df)

  # concatenate all dfs into a single one
  us_data = pd.concat(all_data)
  return us_data

def save_png(us_data, counties, month, day, hour, i):
  fig = px.choropleth(us_data, geojson=counties, locations='FIPS Code', color='Avg Temperature (K)',
                          color_continuous_scale="Jet",
                          range_color=(260, 300),
                          scope="usa",
                          labels={'Avg Temperature (K)':'Temperature (K)'}
                        )
  # make the objects into a datetime obj
  dt = datetime(2022, int(month), day, hour)
  format_dt = dt.strftime("%Y%m%d %H:%M")
  # title = "Temperature: 2022-" + str(month) + "-" + str(day) + " Hour: " + str(hour)
  title = "Temperature: " + format_dt
  fig.update_layout(margin={"r":0,"t":20,"l":0,"b":20},
                    coloraxis_colorbar=dict(lenmode='fraction', len=0.65),
                    title={
                      'text': title,
                      'y': 0.85,  # Adjust the y position of the title
                      # 'x': 0.5,   # Center the title horizontally
                      # 'xanchor': 'center',
                      'yanchor': 'top'
                    }
                    )
  
  pio.write_image(fig, f"plotly_figs/{i:003}.png")
  # fig.show()


def crop_the_figs(directory):
   for file in os.listdir(directory):
      full_path = os.path.join(directory,file)
      command = "convert " + full_path + " -crop 700x375+0+50 " + full_path
      os.system(command)


# loop through the first 14 days of a month, plot the daily data for all 14 days
directory = "/media/kaleb/extraSpace/crop/2022_daily_data/daily_data/2022"
month = "01"
# days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
# days = [1,2,3,4,5,6,7,8,9,10]
days = [1,2,3,4,5]
hours = [0,1,2,3,4,5,6,7,8,9,10,11,
         12,13,14,15,16,17,18,19,20,
         21,22,23]


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
     counties = json.load(response)

us_data = retrieve_us_data(month, days, hours)

i=0
for day in days:
  for hour in hours:
    hour_df = us_data
    hour_df = hour_df[hour_df["Day"] == day]
    hour_df = hour_df[hour_df['Hour'] == hour]
    save_png(hour_df, counties,month,day,hour,i)
    i+=1

# crop the whitespace off the figs
crop_the_figs("plotly_figs")

# save as a gif
os.system("convert -delay 30 plotly_figs/*.png plotly_test.gif")
   