from riotwatcher import LolWatcher, ApiError

lol_watcher = LolWatcher('RGAPI-df3d865e-adc7-4ee4-abbf-495f04e0ec28')

my_region = 'euw1'

me = lol_watcher.summoner.by_name(my_region, 'iXeon')
print(me)
puuid = me.get("puuid")
print("this is puuid")
print(puuid)

# account_stats = by_account(my_region, póg)
# all objects are returned (by default) as a dict
# lets see if i got diamond yet (i probably didnt)
# my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)

# First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']


# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

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