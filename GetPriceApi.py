import requests
from datetime import datetime

def loadauthdata():
    authfile = open('AuthDataFile', 'r') #here u need File with your auth data for Userless access
    clientid = authfile.readline()
    secret = authfile.readline()
    authdata = {'client_id': clientid, 'client_secret': secret, 'v': datetime.now().strftime('%Y%m%d')}
    return authdata

def getcategoryreq(authdata):
    categoryReq = requests.get('https://api.foursquare.com/v2/venues/categories', params=authdata)
    return categoryReq.json()

def getplaceid(location, name, authdata): # find place id from location and name
    authdata['ll']=location
    findrequest = requests.get('https://api.foursquare.com/v2/venues/search', params=authdata)
    venues = findrequest.json()["response"]["venues"]
    for dict in venues:
        if dict.get('name') == name:
            return dict.get('id')

def getvenueinfo(placeid, authdata):
    venueinforeq = requests.get('https://api.foursquare.com/v2/venues/'+placeid+'/', params=authdata)
    info = venueinforeq.json()["response"]["venue"] #now do with it just what u want get those field that u need, ex. price
    return (info["price"]).get('tier') #return tier of price from 1(not expensive) to 4(where is my money) 

#u need to write your own script, it's just example
a = getplaceid('55.766774,37.614918', 'Март', loadauthdata())
print (getvenueinfo(a, loadauthdata()))
