from datetime import datetime
import datetime
from meteostat import Point, Daily
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="GetLoc")

la = input("Enter Location:")
loc = geolocator.geocode(la)

lat = loc.latitude
lon = loc.longitude

location = Point(lat, lon)

today_date = datetime.datetime.today()
one_year_ago = today_date - datetime.timedelta(days=365)

cy = today_date.year
cm = today_date.month
cd = today_date.day

py = one_year_ago.year
pm = one_year_ago.month
pd = one_year_ago.day

ltoday = datetime.datetime(py, pm, pd)
today = datetime.datetime(cy, cm, cd)

data = Daily(location, ltoday, today)
fdata = data.fetch()
data = Daily(location, today, today)
tdata = data.fetch()

fdata['tavg_today'] = fdata['tavg'].shift(-1)
fdata['pres_today'] = fdata['pres'].shift(-1)
fdata['wspd_today'] = fdata['wspd'].shift(-1)

tdata = tdata.fillna(0)
fdata = fdata.fillna(0)

fdata.drop(fdata.index[-1])

features = fdata[['tavg',	'tmin',	'tmax',	'prcp',	'snow',	'wdir',	'wspd',	'wpgt',	'pres',	'tsun']]
targets = fdata[['tavg_today', 'pres_today', 'wspd_today']]

# X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(features, targets)

df = model.predict(tdata)

tavg = df[0][0]
pres = df[0][1]
wspd = df[0][2]

print("Average Temperature:", tavg)
print("Average Precipitation:", pres)
print("Average Wind Speed:", wspd)