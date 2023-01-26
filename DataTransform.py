import requests, json, time, operator, pickle, random

seasons = ['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006']
seasons.reverse()
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min

def main(labels,seasons):
    path = "test123.csv"
    writeCSVHeader(labels,path)
    for season in seasons:
        winnersById = load_obj(season+'winnersById')
        playerIdByTeamID = load_obj(season+'PlayerIdByTeamID')
        seasonAverages = load_obj(season+'SeasonAverages')
        for game in winnersById:
            
            w = winnersById[game]['winner']
            h = winnersById[game]['home']
            v = winnersById[game]['visitor']

            homePlayerIds = playerIdByTeamID[str(h)]
            visitorPlayerIds = playerIdByTeamID[str(v)]
            homeTeam = []
            visitorTeam = []
            for id in homePlayerIds:
                homeTeam.append(seasonAverages[id])
            for id in visitorPlayerIds:
                visitorTeam.append(seasonAverages[id])
            
            bestH = []
            for i in range(0,3):
                b = getBestPlayer(homeTeam)
                min = homeTeam[b][-1]
                min = min.split(':')[0]
                homeTeam[b][-1] = min
                bestH.append(homeTeam[b])
                homeTeam.pop(b)

            bestV = []
            for i in range(0,3):
                b = getBestPlayer(visitorTeam)
                min = visitorTeam[b][-1]
                min = min.split(':')[0]
                visitorTeam[b][-1] = min
                bestV.append(visitorTeam[b])
                visitorTeam.pop(b)
            
            print(game, w, h, v)
            print("home team best players: ", bestH)
            print("visitor team best players: ", bestV)
            path = "test123.csv"
            writeCSV(game,w,bestH,bestV,path)

def writeCSV(game, w,bestH,bestV,path):
    line = str(w)+','+str(game)
    csv = open(path,'a')
    for player in range(len(bestH)):
        for stat in range(len(bestH[player])):
            line += ','+str(bestH[player][stat])
    for player in range(len(bestV)):
        for stat in range(len(bestV[player])):
            line += ','+str(bestV[player][stat])

    csv.write(line+'\n')
    print(line)

def writeCSVHeader(labels, path):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,3):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
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
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)



main(labels,seasons)
