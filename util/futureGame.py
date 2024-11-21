

import requests, json, time, operator, pickle, random


labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']

path = "csv1/futureTest.csv"

season = '2022'

playersPerTeam = 9





def main(**kwargs):

    playerIdByTeamID = load_obj(season+'PlayerIdByTeamID')
    seasonAverages = load_obj(season+'SeasonAverages')
    url = 'https://www.balldontlie.io/api/v1/games/'
    id = '858130'
    writeCSVHeader(labels, path)
    url+=id

    r = req(url)
    homeTeamID = str(r['home_team']['id'])
    visitorTeamID = str(r['visitor_team']['id'])
   # print(len(homeTeamPlayers))
    #print(len(playerIdByTeamID))

    homePlayers = []
    for player in playerIdByTeamID[homeTeamID]:
        homePlayers.append(player)
    visitorPlayers = []
    for player in playerIdByTeamID[visitorTeamID]:
        visitorPlayers.append(player)
    print(homePlayers,visitorPlayers)

    homeTeam = []
    visitorTeam = []

    for id in homePlayers:
        homeTeam.append(seasonAverages[id])
    for id in visitorPlayers:
        visitorTeam.append(seasonAverages[id])



    bestH = []
    bestHomeIds =[]
    for i in range(0,playersPerTeam):
        b = getBestPlayer(homeTeam)
        min = homeTeam[int(b)][-1]
        min = min.split(':')[0]
        homeTeam[b][-1] = min
        bestH.append(homeTeam[b])
        bestHomeIds.append(homePlayers[b])
        homePlayers.pop(b)
        homeTeam.pop(b)

    bestV = []
    bestVisitorIds = []
    for i in range(0,playersPerTeam):
        b = getBestPlayer(visitorTeam)
        min = visitorTeam[int(b)][-1]
        min = min.split(':')[0]
        visitorTeam[b][-1] = min
        bestV.append(visitorTeam[b])
        bestVisitorIds.append(visitorPlayers[b])
        visitorTeam.pop(b)
        visitorPlayers.pop(b)


    print('visitor team:',len(bestV),bestVisitorIds) 
    print('home team:',len(bestH),bestHomeIds) 
    writeCSV(id,homeTeamID,visitorTeamID,bestH,bestV,path)











def writeCSV(game,homeId,visitorId,bestH,bestV,path):
    line = str(game)+','+str(homeId)+','+str(visitorId)
    for player in range(len(bestH)):
        for stat in range(len(bestH[player])):
            line += ','+str(bestH[player][stat])
    for player in range(len(bestV)):
        for stat in range(len(bestV[player])):
            line += ','+str(bestV[player][stat])


    
    csv = open(path,'a')
    csv.write(line+'\n')
    print(line)

def writeCSVHeader(labels, path,**kwargs):
    header = 'gameid,home_id,visitor_id'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,playersPerTeam):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    return header




def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

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
    time.sleep(1.5)
    return r.json()
 
def getBestPlayer(team):
    best = ''
    topMin = 0
    for player in range(len(team)):

        if len(team[player]) == 0:
            continue
        min = team[player][-1]
        min = min.split(':')[0]
        #print(min,topMin)
        if int(min) > int(topMin):
            best = player
            topMin = min
    return best



main()
