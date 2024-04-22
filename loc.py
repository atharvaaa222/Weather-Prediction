from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="GetLoc")

la = input("Enter Location:")
location  = geolocator.geocode(la)

lat = location.latitude
lon = location.longitude
print(lat)
print(lon)


