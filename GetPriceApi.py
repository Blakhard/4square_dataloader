import requests
from datetime import datetime
import re
from random import randint
from transliterate import slugify

def loadauthdata():
    authfile = open('AuthDataFile', 'r')
    clientid = authfile.readline()
    secret = authfile.readline()
    authfile.close()
    authdata = {'client_id': clientid, 'client_secret': secret, 'v': datetime.now().strftime('%Y%m%d')}
    return authdata

def getcategoryreq(authdata):
    categoryReq = requests.get('https://api.foursquare.com/v2/venues/categories', params=authdata)
    return categoryReq.json()

def getplaceid(location, name, authdata):
    authdata['ll']=location
    findrequest = requests.get('https://api.foursquare.com/v2/venues/search', params=authdata)
    venues = findrequest.json()["response"]["venues"]
    temp = textprepairer(name)
    for dict in venues:
        n = dict.get('name').lower()
        if (temp[0] in n) or (temp[1] in n):
            print(dict.get('id'))
            if dict.get('price'):
                return dict.get('price')
            else:
                return dict.get('id')

def getvenueinfo(placeid, authdata):
    venueinforeq = requests.get('https://api.foursquare.com/v2/venues/'+placeid+'/', params=authdata)
    info = venueinforeq.json()["response"]["venue"] #now do with it just what u want
    try:
        return (info["price"]).get('tier')
    except:
        return randint(1,3)

def textprepairer(text): #func that prepare text from db to format we need
    if '«' in text:
        temp = re.search(r'«(\w+(.\w)*)»', text)
        return [(temp.group(1)).lower(), (slugify((temp.group(1)).lower()).replace('-', ' '))]
    else:
        return [text.lower(), ((slugify(text)).lower()).replace('-', ' ')]

temp = getplaceid('55.857319,37.432131', 'Corneli Pizza', loadauthdata())
print(getvenueinfo(temp, loadauthdata()))
