import foursquare, time

client = foursquare.Foursquare(
    client_id='Y1CPCQJRBWVHOPPLP1IHFWVYRSIGKNDY4PN32X1OWCSAVVPN',
    client_secret='1CEWCHG0YU00VP1JZ4P0T0VRNOX43FB2IIUE3G1F511TEGRX'
)

def venues_by_cityname(cityname):
    params = dict(near=cityname)
    try:
        data = client.venues.search(params=params)
        return sorted([v['id'] for v in data['venues']])
    except foursquare.FailedGeocode:
        return None
    except foursquare.ServerError:
        time.sleep(60)
        return venues_by_cityname(cityname)