import requests, json, time, operator, pickle, random
#seasons = ['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005']
seasons = ['2019']
seasons.reverse()
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
playersPerTeam = 5

def main(labels,seasons,**kwargs):    
    for season in seasons:
        print('Season:', season)

        games = load_obj(season+'Games')
        playerIdByTeamID = load_obj(season+'PlayerIdByTeamID')
        seasonAverages = load_obj(season+'SeasonAverages')

        for game in games:
            
            g=games[game]
            print(game, g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])

            homePlayerIds = playerIdByTeamID[str(g['home_id'])]
            visitorPlayerIds = playerIdByTeamID[str(g['visitor_id'])]
            homeTeam = []
            visitorTeam = []
            for id in homePlayerIds:
                homeTeam.append(seasonAverages[id])
            for id in visitorPlayerIds:
                visitorTeam.append(seasonAverages[id])
            
            bestH = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(homeTeam)
                min = homeTeam[b][-1]
                min = min.split(':')[0]
                homeTeam[b][-1] = min
                bestH.append(homeTeam[b])
                homeTeam.pop(b)

            bestV = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(visitorTeam)
                min = visitorTeam[b][-1]
                min = min.split(':')[0]
                visitorTeam[b][-1] = min
                bestV.append(visitorTeam[b])
                visitorTeam.pop(b)





def writeCSV(game, w,bestH,bestV,path):
    line = str(w)+','+str(game)
    for player in range(len(bestH)):
        for stat in range(len(bestH[player])):
            line += ','+str(bestH[player][stat])
    for player in range(len(bestV)):
        for stat in range(len(bestV[player])):
            line += ','+str(bestV[player][stat])


    foo = random.randint(0,20)
    if foo == 10:
        csv = open('test.csv','a')
        csv.write(line+'\n')
        return ''
    csv = open(path,'a')
    csv.write(line+'\n')
    print(line)

def writeCSVHeader(labels, path):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,5):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    csv = open('test.csv','w')
    csv.write(header+'\n')
    return header




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
 




main(labels,seasons)


