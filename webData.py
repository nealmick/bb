import requests, json, time, operator, pickle, random
import pandas as pd
from datetime import datetime,timezone
seasons = ['2020','2019','2018','2017','2016','2015','2014','2013','2012']

#seasonsCSV = ['2018-19','2017-18','2016-17','2015-16','2014-15','2013-14']#,'2012-13','2011-12']
#seasonsCSV.reverse()

seasons.reverse()

labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
playersPerTeam = 7
path = "csv/train.csv"
numgames = 500
def CreateDataset(seasons,numgames,**kwargs):
    writeCSVHeader(labels, path)
    
    numnotfound = 0
    for s in range(len(seasons)):
        season=seasons[s]
        #seasonCSV=seasonsCSV[s]
        print('Season:', season)
        teamNamesById = load_obj('teamNamesById')
        teamAbvById = load_obj('teamAbvById')
        nba_api_teamids = load_obj("apiTeamIdsByAbv")
        games = load_obj(season+'Games')
        playerIdByTeamID = load_obj(season+'PlayerIdByTeamID')
        seasonAverages = load_obj(season+'SeasonAverages')
        #df = pd.read_excel('../Odds-Data-Clean/'+seasonCSV+'.xlsx')
        #f = df.to_dict()
        foo = 0
        c = 0
        count = 0

        sorted = sortGames(games)
        games = load_obj(season+'Games')
        streaks = {}
        for num in range(1,31):
            streaks[int(num)] = 0

        for game in sorted:
            #print(game, game in games)
            #print(games[game]['date'])
            #print(games[game]['spread'])
            count+=1
            g=games[game]
            print(game,g['spread'], g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])
            print('spread:',g['spread'],' vscore-hscore:',g['visitor_score']-g['home_score'])
            print()


            beforeStreaks = streaks.copy()
            if g['home_score'] > g['visitor_score']:
                if streaks[(g['home_id'])] < 0:
                    streaks[g['home_id']] = 0
                else:
                    streaks[g['home_id']] += 1
                if streaks[g['visitor_id']] > 0:
                    streaks[g['visitor_id']] = 0
                else:
                    streaks[g['visitor_id']] -= 1
            if g['home_score'] < g['visitor_score']:
                if streaks[g['home_id']] < 0:
                    streaks[g['home_id']] = 0
                else:
                    streaks[g['home_id']] -= 1
                if streaks[g['visitor_id']] > 0:
                    streaks[g['visitor_id']] = 0
                else:
                    streaks[g['visitor_id']] += 1




            if g['spread'] == '':
                print('noSpread')
                count-=1
                continue
            elif g['visitor_score']-g['home_score'] < 0 and g['spread'] <0:
                c+=1
                print('correct')

            elif g['visitor_score']-g['home_score'] > 0 and g['spread'] >0:
                c+=1
                print('correct')
            else:
                print('wrong')
            print('percent winner agrees with spread%',c/count*100)

            try:
                homeTeamStats = g['homeTeamStats']
                visitorTeamStats =g['visitorTeamStats']
            except KeyError:
                print('# stats not found-------------',numnotfound)
                numnotfound+=1
                continue
            print('GP, W , L',homeTeamStats,visitorTeamStats)
            homePlayerIds = playerIdByTeamID[str(g['home_id'])]
            visitorPlayerIds = playerIdByTeamID[str(g['visitor_id'])]
            homeTeam = []
            visitorTeam = []

            for player in g['data']:
                if player['player'] is None:
                    continue
    
                if player['pts']!= 0 or player['reb'] != 0 or player['stl'] != 0 or player['blk'] != 0 or player['pf'] != 0:
                    try:
                        
                            if int(player['team']['id']) == int(g['home_id']):
                                homeTeam.append(seasonAverages[int(player['player']['id'])])
                            elif int(player['team']['id']) == int(g['visitor_id']):
                                visitorTeam.append(seasonAverages[int(player['player']['id'])])
                            else:
                                print('dddddddddddidnt match team')
                    except KeyError:
                        data = getSeaonAverage(int(player['player']['id']),season,labels)
                        seasonAverages.update({int(player['player']['id']):data})
                        save_obj(seasonAverages,season+'SeasonAverages')
                        print('error')
                
            '''

                
            
            for id in homePlayerIds:
                homeTeam.append(seasonAverages[id])
            for id in visitorPlayerIds:
                visitorTeam.append(seasonAverages[id])
            '''

            print(len(visitorTeam),len(homeTeam),'--------------------------------------------------')
            
            if(len(visitorTeam)<playersPerTeam or len(homeTeam)<playersPerTeam):
                print(len(visitorTeam),len(homeTeam),' found game with too few players--------------------------------------------------')
                continue
            bestH = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(homeTeam)
                min = homeTeam[int(b)][-1]
                min = min.split(':')[0]
                homeTeam[b][-1] = min
                bestH.append(homeTeam[b])
                homeTeam.pop(b)

            bestV = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(visitorTeam)
                min = visitorTeam[int(b)][-1]
                min = min.split(':')[0]
                visitorTeam[b][-1] = min
                bestV.append(visitorTeam[b])
                visitorTeam.pop(b)
            foo+=1
            writeCSV(game,g['spread'],g['home_score'],g['visitor_score'],g['home_id'],g['visitor_id'],homeTeamStats,visitorTeamStats,bestH,bestV,path,season,foo,beforeStreaks,numgames,sorted)


def writeCSV(game,spread, homeScore,visitorScore,homeId,visitorId,homeTeamStats,visitorTeamStats,bestH,bestV,path,season,foo,streaks,numgames,sorted):
    line = str(homeScore)+','+str(visitorScore)+','+str(game)+','+str(spread)+','+str(homeId)+','+str(streaks[int(homeId)])
    for stat in homeTeamStats:
        line+=','+str(stat)
    line += ','+str(visitorId)+','+str(streaks[int(visitorId)])
    for stat in visitorTeamStats:
        line+=','+str(stat)
    for player in range(len(bestH)):
        for stat in range(len(bestH[player])):
            line += ','+str(bestH[player][stat])
    for player in range(len(bestV)):
        for stat in range(len(bestV[player])):
            line += ','+str(bestV[player][stat])
    


    if season == '2020':
        if foo > len(sorted)-numgames:#sets split of test/train on final season.....
            csv = open('csv/test.csv','a')
            csv.write(line+'\n')
            return ''
        #return ''#uncomment to not train on same season as test

    csv = open(path,'a')
    csv.write(line+'\n')
    #print(line)

def writeCSVHeader(labels, path,**kwargs):
    header = 'home_score,visitor_score,gameid,spread,home_id,home_streak,hgp,hw,hl,visitor_id,visitor_streak,vgp,vw,vl'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,playersPerTeam):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    csv = open('csv/test.csv','w')
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



def sortGames(games):
    gCopy = games
    sorted = []

    while len(gCopy) > 0 :
        current = ''
        currentID = ''
        
        for game in gCopy:
            #print(game)
            #print(games[game]['date'])
            if games[game]['date'] > current:
                current = games[game]['date']
                currentID = game
        
        #print(games[currentID]['date'])   
        sorted.append(currentID)     
        gCopy.pop(currentID)
    sorted.reverse()
    return sorted

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
    if str(r) != '<Response [200]>':#means we request too fast..
        time.sleep(30)
        req(url)
    time.sleep(1.5)
    return r.json()
 

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


#CreateDataset(seasons,numgames)

