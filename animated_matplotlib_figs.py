from metpy.plots import USSTATES, USCOUNTIES
import cartopy.crs as ccrs
from shapely.geometry import Point 
from matplotlib.cm import ScalarMappable
import pandas as pd
import matplotlib.pyplot as plt
import os

year_dir = "/media/kaleb/extraSpace/2022_daily_data/2022/"
yyyymmdd = "20220101"
param = 'Avg Temperature (K)'

all_data = []
month = yyyymmdd[4:6]
day = yyyymmdd[6:8]

for state_dir in os.listdir(year_dir):
    state_path = os.path.join(year_dir, state_dir)

    # iteratore over the files in the dir
    for file in os.listdir(state_path):

        # if the filename has the month we're looking for
        # searchstring = month + '.csv'
        # if searchstring in file:
        file_path = os.path.join(state_path, file) # full path to file
        df = pd.read_csv(file_path, index_col=False)

        # to minimize space, only append the necessary columns
        df['Lat'] = (df['Lat (llcrnr)'] + df['Lat (urcrnr)']) / 2
        df['Lon'] = (df['Lon (llcrnr)'] + df['Lon (urcrnr)']) / 2

        # df['Day'] = pd.to_numeric(df['Day']) # convert to int if stored as str
        # df = df[df['Day'] == day]

        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])

        df = df[['Date', 'Lat', 'Lon', param]]
        all_data.append(df)

combined_df = pd.concat(all_data)
combined_df = combined_df.reset_index(drop=True)

df = combined_df
df = df.sort_values(by=['Date'])

sorted_df = df.set_index('Date')
new_df = sorted_df['2022-01-10':'2022-01-15']
new_df.reset_index(inplace=True)
df = new_df

df_arr = [group for _, group in df.groupby(pd.Grouper(key='Date', freq='H'))]

lon_min, lon_max = combined_df['Lon'].min(), combined_df['Lon'].max()
lat_min, lat_max = combined_df['Lat'].min() - 3, combined_df['Lat'].max()

# calculate the average to find the center
lat_avg, lon_avg = combined_df['Lat'].mean(), combined_df['Lon'].mean()
extent = [lon_min + 5, lon_max - 8, lat_min + 1, lat_max]


i=0
for d in df_arr:
    proj = ccrs.LambertConformal(central_longitude=lon_avg, central_latitude=lat_avg) # center the spherical orientation
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection=proj)
    ax.set_extent(extent, ccrs.Geodetic())
    ax.add_feature(USSTATES.with_scale('5m'))

    cmap = plt.cm.get_cmap('jet') # viridis, plasma, cool, jet, twilight_shifted, greys
    ax.scatter(d['Lon'], d['Lat'], c=d[param],
            cmap=cmap, transform=ccrs.PlateCarree(), s=1)

    sm = ScalarMappable(cmap=cmap)
    sm.set_array(d[param])
    sm.set_clim(vmin=260, vmax=300)
    plt.colorbar(sm, ax=ax, pad=0.01, shrink=0.55, ticks=[260, 270, 280, 290, 300], 
                label=param)
    plt.title(param + '\nDate: ' + str(d['Date'].iloc[0]))
    plt.tight_layout()
    plt.savefig(f'wrf/{i:003}')
    plt.close()
    i+=1

os.system("convert -delay 20 wrf/*.png wrf_tmp_winter.gif")

###########################################################################
##########################################################################
# spring
new_df = sorted_df['2022-04-02':'2022-04-07']
new_df.reset_index(inplace=True)
df = new_df

df_arr = [group for _, group in df.groupby(pd.Grouper(key='Date', freq='H'))]

lon_min, lon_max = combined_df['Lon'].min(), combined_df['Lon'].max()
lat_min, lat_max = combined_df['Lat'].min() - 3, combined_df['Lat'].max()

# calculate the average to find the center
lat_avg, lon_avg = combined_df['Lat'].mean(), combined_df['Lon'].mean()
extent = [lon_min + 5, lon_max - 8, lat_min + 1, lat_max]


i=0
for d in df_arr:
    proj = ccrs.LambertConformal(central_longitude=lon_avg, central_latitude=lat_avg) # center the spherical orientation
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection=proj)
    ax.set_extent(extent, ccrs.Geodetic())
    ax.add_feature(USSTATES.with_scale('5m'))

    cmap = plt.cm.get_cmap('jet') # viridis, plasma, cool, jet, twilight_shifted, greys
    ax.scatter(d['Lon'], d['Lat'], c=d[param],
            cmap=cmap, transform=ccrs.PlateCarree(), s=1)

    sm = ScalarMappable(cmap=cmap)
    sm.set_array(d[param])
    sm.set_clim(vmin=260, vmax=300)
    plt.colorbar(sm, ax=ax, pad=0.01, shrink=0.55, ticks=[260, 270, 280, 290, 300], 
                label=param)
    plt.title(param + '\nDate: ' + str(d['Date'].iloc[0]))
    plt.tight_layout()
    plt.savefig(f'wrf/{i:003}')
    plt.close()
    i+=1

os.system("convert -delay 20 wrf/*.png wrf_tmp_spring.gif")

###########################################################################
##########################################################################
# summer
new_df = sorted_df['2022-08-02':'2022-08-08']
new_df.reset_index(inplace=True)
df = new_df

df_arr = [group for _, group in df.groupby(pd.Grouper(key='Date', freq='H'))]

lon_min, lon_max = combined_df['Lon'].min(), combined_df['Lon'].max()
lat_min, lat_max = combined_df['Lat'].min() - 3, combined_df['Lat'].max()

# calculate the average to find the center
lat_avg, lon_avg = combined_df['Lat'].mean(), combined_df['Lon'].mean()
extent = [lon_min + 5, lon_max - 8, lat_min + 1, lat_max]


i=0
for d in df_arr:
    proj = ccrs.LambertConformal(central_longitude=lon_avg, central_latitude=lat_avg) # center the spherical orientation
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection=proj)
    ax.set_extent(extent, ccrs.Geodetic())
    ax.add_feature(USSTATES.with_scale('5m'))

    cmap = plt.cm.get_cmap('jet') # viridis, plasma, cool, jet, twilight_shifted, greys
    ax.scatter(d['Lon'], d['Lat'], c=d[param],
            cmap=cmap, transform=ccrs.PlateCarree(), s=1)

    sm = ScalarMappable(cmap=cmap)
    sm.set_array(d[param])
    sm.set_clim(vmin=260, vmax=300)
    plt.colorbar(sm, ax=ax, pad=0.01, shrink=0.55, ticks=[260, 270, 280, 290, 300], 
                label=param)
    plt.title(param + '\nDate: ' + str(d['Date'].iloc[0]))
    plt.tight_layout()
    plt.savefig(f'wrf/{i:003}')
    plt.close()
    i+=1

os.system("convert -delay 20 wrf/*.png wrf_tmp_summer.gif")


###########################################################################
##########################################################################
# fall
new_df = sorted_df['2022-10-01':'2022-10-05']
new_df.reset_index(inplace=True)
df = new_df

df_arr = [group for _, group in df.groupby(pd.Grouper(key='Date', freq='H'))]

lon_min, lon_max = combined_df['Lon'].min(), combined_df['Lon'].max()
lat_min, lat_max = combined_df['Lat'].min() - 3, combined_df['Lat'].max()

# calculate the average to find the center
lat_avg, lon_avg = combined_df['Lat'].mean(), combined_df['Lon'].mean()
extent = [lon_min + 5, lon_max - 8, lat_min + 1, lat_max]


i=0
for d in df_arr:
    proj = ccrs.LambertConformal(central_longitude=lon_avg, central_latitude=lat_avg) # center the spherical orientation
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection=proj)
    ax.set_extent(extent, ccrs.Geodetic())
    ax.add_feature(USSTATES.with_scale('5m'))

    cmap = plt.cm.get_cmap('jet') # viridis, plasma, cool, jet, twilight_shifted, greys
    ax.scatter(d['Lon'], d['Lat'], c=d[param],
            cmap=cmap, transform=ccrs.PlateCarree(), s=1)

    sm = ScalarMappable(cmap=cmap)
    sm.set_array(d[param])
    sm.set_clim(vmin=260, vmax=300)
    plt.colorbar(sm, ax=ax, pad=0.01, shrink=0.55, ticks=[260, 270, 280, 290, 300], 
                label=param)
    plt.title(param + '\nDate: ' + str(d['Date'].iloc[0]))
    plt.tight_layout()
    plt.savefig(f'wrf/{i:003}')
    plt.close()
    i+=1

os.system("convert -delay 20 wrf/*.png wrf_tmp_fall.gif")