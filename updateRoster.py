


import requests, json, time, operator, pickle, random

labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
season = '2022'
roster = {}
for i in range(0,31):
    roster.update({str(i):[]})

def main():
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    #avg = getSeaonAverage('61',season,labels)
    #print(avg)
    #iterate team in teams
    for team in playerIdByTeamID:
        #iterate player in teams
        for playerid in playerIdByTeamID[team]:
            #get current team
            teamid = getCurrentTeam(playerid,season)
            #add player to roster
            roster[str(teamid)].append(playerid)
            print(roster)
            #save roster
            save_obj(roster,'roster')

def getSeaonAverage(playerId,season,labels):
    url = 'https://www.balldontlie.io/api/v1/season_averages?season='+season
    url+='&player_ids[]='+str(playerId)
    r = req(url)
    if len(r['data'])==0:
        print('no season average-----------------')
        return []
    r = r['data'][0]
    print(r)
    seasonAverage = []
    for label in labels:
        seasonAverage.append(r[label])
    return seasonAverage


def getCurrentTeam(playerId,season):
    url = 'https://www.balldontlie.io/api/v1/players/'+str(playerId)
    r = req(url)
    return r['team']['id']
        

def req(url):
    proxy = load_obj('proxy')
    dict = {}
    p = random.randint(0,len(proxy)-1)
    dict.update({'http' : proxy[p]})
    r = requests.get(url)
    print('proxy: ', proxy[p], 'url: ', url, 'response: ', r)
    if str(r) != '<Response [200]>':#means we request too fast..fast af boi so like anything under 1 r/sec cause error at 60 seconds in....
        time.sleep(30)
        req(url)
    time.sleep(2)

    return r.json()

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

main()
