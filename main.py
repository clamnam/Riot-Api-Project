from riotwatcher import LolWatcher, ApiError
import requests
import http.client
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)





allgamedata = http.client.HTTPSConnection('localhost:8888')
print(allgamedata)

allgamedata.request("GET", "/liveclientdata/allgamedata")

response = allgamedata.getresponse()

data = response.read()
print (data)

lol_watcher = LolWatcher('RGAPI-48be5475-5402-4a6f-bec0-6651a68becbd')
my_region = 'euw1'
my_region_full = 'europe'
my_name = 'RubyCabs'

print("/////////////////////////////My data///////////////////////////////////")
me = lol_watcher.summoner.by_name(my_region, my_name)
print(me)
print("/////////////////////////////My PUUID///////////////////////////////////")
puuid = me.get("puuid")
print(puuid)
print("/////////////////////////////List of Matches///////////////////////////////////")
matchlist = lol_watcher.match.matchlist_by_puuid(my_region_full, puuid, 0, 20, 420, None, None, None)
print(matchlist)
print("/////////////////////////////Most Recent Match///////////////////////////////////")
recentMatch = matchlist[0]
match = lol_watcher.match.by_id(my_region,recentMatch )
print(match)

print("/////////////////////////////Live Data///////////////////////////////////")
liveData = requests.get("https://localhost:8888/liveclientdata/allgamedata", verify=False)
print(liveData.content)

try:
    response = lol_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise