import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.dates as mdates


def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()


#leaflet_plot_stations(400, 'a955866f3e9b5bb2c8cdfc366f8eb6ce3d4e1b3430ead0439e7b3a38')
leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
#leaflet_plot_stations(400,'0006c7fbfba4168a4393f4027f64594d8e1062383372f83ce8f7b620')

pd.set_option('display.max_rows', None)
#mplleaflet.display()
hashid = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'
binsize = 400
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d{}/{}.csv'.format(binsize, hashid))
df['datetime'] = df['Date'].apply(pd.to_datetime)
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['Data_Value'] = pd.to_numeric(df['Data_Value'])/10
#print(df.dtypes)

func = lambda x : pd.offsets.DateOffset(years=2012-x)
df['convertedDate'] =  df['datetime'] + df['year'].apply(func)
#print(df)

d2015 = df[(df['datetime'] >= '2015-01-01') & (df['datetime'] < '2016-01-01')]
df = df[(df['datetime'] >= '2005-01-01') & (df['datetime'] < '2015-01-01')]
high = df[df['Element']=='TMAX']
low = df[df['Element']=='TMIN']

#datetime(1985,7,1), datetime(2015,7,1), timedelta(days=1)

#x = np.arange('2005-01-01','2014-12-31',dtype='datetime64[D]')
#x = list(map(pd.to_datetime, x ))
high = high.groupby(by='convertedDate').max()
high = high.reset_index()
#high['datetime'] = high['Date'].apply(pd.to_datetime)
high.sort_values(by='convertedDate')
#print(high)
#high = high[(high['datetime'] > '2014-01-01') & (high['datetime'] < '2015-01-01')]
low = low.groupby(by='convertedDate').min()
low = low.reset_index()
#low['datetime'] = low['Date'].apply(pd.to_datetime)
low.sort_values(by='convertedDate')
#low = low[(low['datetime'] > '2014-01-01') & (low['datetime'] < '2015-01-01')]
#x = x[(x > '2014-01-01') & (x < '2015-01-01')]
print(len(low), len(high))
m = pd.merge(high, low, how='outer', on='convertedDate')
#print(m)
#print(m[pd.isnull(m['datetime'])])
m = m.groupby(by='convertedDate').agg({'Data_Value_x':'max','Data_Value_y':'min'})
m = m.reset_index()
#print(m.dtypes)
#m['Data_Value_x','Data_Value_y'] = m['Data_Value_x','Data_Value_y'].astype({'Data_Value_x':float,'Data_Value_y':float})
#m['Data_Value_x']= pd.to_numeric(m['Data_Value_x'], downcast='float', errors='coerce')
#m['Data_Value_y']= pd.to_numeric(m['Data_Value_y'], downcast='float', errors='coerce')


#locs, labels = plt.xticks()
#print(locs)
#print(labels)
#print(m)
plt.figure(figsize=(20,8))
#m = m[(m['convertedDate'] > '2013-01-01') & (m['datetime'] < '2014-01-01')]
plt.plot(m['convertedDate'], m['Data_Value_x'], label='max 2005-2014')
plt.plot(m['convertedDate'], m['Data_Value_y'], label='min 2005-2014')
plt.xlabel('day of the year')
plt.ylabel('temperature $^\circ$ C')
plt.title('Min and Max temperatures in Ann Arbor, Michigan, United States between 2005-2015')
#print(m.dtypes)
d = m['convertedDate'].values
#print(fig.figsize())
#print(d)
plt.gca().fill_between(d, m['Data_Value_x'],m['Data_Value_y'],facecolor='grey', alpha=0.5)

# Set the locator
locator = mdates.MonthLocator(interval=1)  # every month
# Specify the format - %b gives us Jan, Feb...
fmt = mdates.DateFormatter('%b')

plt.gca().xaxis.set_major_formatter(fmt)
plt.gca().xaxis.set_major_locator(locator)
#month_abbr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#plt.gca().set_xticklabels([s for s in month_abbr if s!=''])




d2015['max_value']=d2015['Data_Value']
d2015['min_value']=d2015['Data_Value']
d2015 = d2015.groupby(by='convertedDate').agg({'max_value':max, 'min_value':min,'Data_Value':np.mean})
d2015 = d2015.reset_index()
s2015 = pd.merge(m, d2015, on='convertedDate', how='left')
#print(s2015)

s2015max = s2015[(s2015['max_value'] > s2015['Data_Value_x']) ]
s2015min = s2015[(s2015['min_value'] < s2015['Data_Value_y']) ]
#print(s2015)
sdmax = s2015max['convertedDate'].values   
sdmin = s2015min['convertedDate'].values 
plt.scatter(sdmax, s2015max['max_value'], s=50, color='b', label='2015 above max')
plt.scatter(sdmin, s2015min['min_value'], s=50, color='r', label='2015 below min')
plt.legend(loc='lower center', frameon=False)
plt.show()
plt.savefig('minmaxtmpr.png')

