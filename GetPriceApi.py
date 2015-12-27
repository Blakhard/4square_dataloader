import requests
from datetime import datetime

def loadauthdata():
    authfile = open('AuthDataFile', 'r')
    clientid = authfile.readline()
    secret = authfile.readline()
    authdata = {'client_id': clientid, 'client_secret': secret, 'v': datetime.now().strftime('%Y%m%d')}
    return authdata

def getcategoryreq(authdata):
    categoryReq = requests.get('https://api.foursquare.com/v2/venues/categories', params=authdata)
    return categoryReq.json()

def getplaceid(location, name, authdata):
    authdata['ll']=location
    findrequest = requests.get('https://api.foursquare.com/v2/venues/search', params=authdata)
    venues = findrequest.json()["response"]["venues"]
    for dict in venues:
        if dict.get('name') == name: # c is не работает
            return dict.get('id')

def getvenueinfo(placeid, authdata):
    venueinforeq = requests.get('https://api.foursquare.com/v2/venues/'+placeid+'/', params=authdata)
    info = venueinforeq.json()["response"]["venue"] #now do with it just what u want
    return (info["price"]).get('tier')

a = getplaceid('55.766774,37.614918', 'Март', loadauthdata())
print (getvenueinfo(a, loadauthdata()))
