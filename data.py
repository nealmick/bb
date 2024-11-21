
import requests, json, time, operator, pickle, random
import pandas as pd
from datetime import datetime,timezone


#seasons scanned for data
#'2022'
seasons = ['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011']#,'2010','2009']
#reverse seasons so we start at older season
seasons.reverse()
#player data stat labels
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
#how many players on each team 
playersPerTeam = 7
#path to training csv file
path = "csv/train.csv"


def main(labels,seasons,**kwargs):
    #write csv header
    writeCSVHeader(labels, path)
    #counters for number of error games thrown out.
    pc =0
    numnotfound = 0

    #iterate over seasons
    for s in range(len(seasons)):
        lastGame = {}
        lastGame2 = {}
        lastGame3 = {}
        for num in range(1,31):
            lastGame[int(num)] = None
            lastGame2[int(num)] = None
            lastGame3[int(num)] = None
        #set current season
        season=seasons[s]
        #seasonCSV=seasonsCSV[s]
        print('Season:', season)
        #load saved data
        teamNamesById = load_obj('teamNamesById')
        teamAbvById = load_obj('teamAbvById')
        nba_api_teamids = load_obj("apiTeamIdsByAbv")
        games = load_obj(season+'Games')
        playerIdByTeamID = load_obj(season+'PlayerIdByTeamID')
        seasonAverages = load_obj(season+'SeasonAverages')
        #df = pd.read_excel('../Odds-Data-Clean/'+seasonCSV+'.xlsx')
        #f = df.to_dict()
        #counters
        foo = 0
        c = 0
        count = 0
        #sort games by game date so we can add up win/loss/streak
        sorted = sortGames(games)
        #load this seasons games
        games = load_obj(season+'Games')
        #init streaks dict
        streaks = {}
        for num in range(1,31):
            streaks[int(num)] = 0
        #iterated sorted games in seasons
        for game in sorted:

            #set game counter and print stuff
            count+=1
            g=games[game]
            print(game,g['spread'], g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])
            print('spread:',g['spread'],' vscore-hscore:',g['visitor_score']-g['home_score'])
            hLastGame = None
            hLastGame2 = None
            hLastGame3 = None
            vLastGame = None
            vLastGame2 = None
            vLastGame3 = None

            
            if lastGame[g['home_id']] != None and lastGame[g['visitor_id']] != None and lastGame2[g['home_id']] != None and lastGame2[g['visitor_id']] != None and lastGame3[g['home_id']] != None and lastGame3[g['visitor_id']] != None:
                print('found last game v:', lastGame[g['visitor_id']],' h:',lastGame[g['home_id']])
                for _game in games:
                    if _game == lastGame[g['visitor_id']]:
                        vLastGame = games[_game]

                    if  _game == lastGame2[g['visitor_id']]:
                        vLastGame2 = games[_game]

                    if  _game == lastGame3[g['visitor_id']]:
                        vLastGame3 = games[_game]

                    if _game == lastGame[g['home_id']]:
                        hLastGame = games[_game]

                    if  _game == lastGame2[g['home_id']]:
                        hLastGame2 = games[_game]

                    if  _game == lastGame3[g['home_id']]:
                        hLastGame3 = games[_game]

                if hLastGame is None or vLastGame is None or hLastGame2 is None or vLastGame2 is None or hLastGame3 is None or vLastGame3 is None:
                    print('error ------------++++--------++++-------')
                    continue
                
                home_history = formLastGame(hLastGame,g['home_id'])
                visitor_history = formLastGame(vLastGame,g['visitor_id'])

                home_history2 = formLastGame(hLastGame2,g['home_id'])
                visitor_history2 = formLastGame(vLastGame2,g['visitor_id'])


                home_history3 = formLastGame(hLastGame3,g['home_id'])
                visitor_history3 = formLastGame(vLastGame3,g['visitor_id'])

                try:
                    for player in range(len(home_history[1])):
                            print(home_history[0][player])
                            print(home_history[1][player])
                            print(visitor_history[0][player])
                            print(visitor_history[1][player])
                    print('home history score: ',home_history[2],home_history[3])
                    print('visitor history score: ',visitor_history[2],visitor_history[3])
                except IndexError:
                    continue
            else:
                lastGame3[g['home_id']] = lastGame2[g['home_id']]
                lastGame3[g['visitor_id']] = lastGame2[g['visitor_id']]
                lastGame2[g['home_id']] = lastGame[g['home_id']]
                lastGame2[g['visitor_id']] = lastGame[g['visitor_id']]
                lastGame[g['home_id']] = game
                lastGame[g['visitor_id']] = game
                continue

            #no spread skip game.
            if g['spread'] == 0 or g['spread']== '':
                continue
            #flip spread if season 2022
            if season == '2022':
                g['spread'] = g['spread']*-1
            else:
                g['spread'] = round(float(g['spread']))

            #make streaks copy before updating new streaks with this game
            beforeStreaks = streaks.copy()
            #update streaks based on winner
            if g['home_score'] > g['visitor_score']:
                if streaks[(g['home_id'])] < 0:
                    streaks[g['home_id']] = 1
                else:
                    streaks[g['home_id']] += 1
                if streaks[g['visitor_id']] > 0:
                    streaks[g['visitor_id']] = -1
                else:
                    streaks[g['visitor_id']] -= 1
                    
            if g['home_score'] < g['visitor_score']:
                if streaks[g['home_id']] > 0:
                    streaks[g['home_id']] = -1
                else:
                    streaks[g['home_id']] -= 1
                if streaks[g['visitor_id']] < 0:
                    streaks[g['visitor_id']] += 1
                else:
                    streaks[g['visitor_id']] = 1


            #check no spread, and spread winner
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
            #load home team and visitor team stats
            try:
                homeTeamStats = g['homeTeamStats']
                visitorTeamStats =g['visitorTeamStats']
            except KeyError:
                print('# stats not found-------------',numnotfound)
                numnotfound+=1
                continue
            #print game stats
            print('GP, W , L',homeTeamStats,visitorTeamStats)
            #set home and visitor rosters of player id's
            homePlayerIds = playerIdByTeamID[str(g['home_id'])]
            visitorPlayerIds = playerIdByTeamID[str(g['visitor_id'])]
            homeTeam = []
            visitorTeam = []
            #iterate over player in game request
            for player in g['data']:
                #check if player actually played, or if data is None or not set...
                if player['pts']!= 0 or player['reb'] != 0 or player['stl'] != 0 or player['blk'] != 0 or player['pf'] != 0 or player['player'] is None or player['pts'] == None:
                    try:
                            try:
                            
                                if int(player['team']['id']) == int(g['home_id']):# add player to home team
                                    homeTeam.append(seasonAverages[int(player['player']['id'])])
                                elif int(player['team']['id']) == int(g['visitor_id']):# add player to home team
                                    visitorTeam.append(seasonAverages[int(player['player']['id'])])
                                else:
                                    print('dddddddddddidnt match team')
                            except TypeError:
                                continue
                    except KeyError:
                        #get season averages if we dont already have them
                        data = getSeaonAverage(int(player['player']['id']),season,labels)
                        seasonAverages.update({int(player['player']['id']):data})
                        save_obj(seasonAverages,season+'SeasonAverages')
                        print('error')

                
   
            #if less then 7 players were reported in game, dont use game
            print(len(visitorTeam),len(homeTeam),'--------------------------------------------------')
            if(len(visitorTeam)<7 or len(homeTeam)<7):

                continue
                print(len(visitorTeam),len(homeTeam),' found game with too few players--------------------------------------------------')
                homeTeam = []
                visitorTeam=[]

                for id in homePlayerIds:
                    homeTeam.append(seasonAverages[id])
                for id in visitorPlayerIds:
                    visitorTeam.append(seasonAverages[id])
  
            #get best 7 players for home team
            bestH = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(homeTeam)
                min = homeTeam[int(b)][-1]
                min = min.split(':')[0]
                homeTeam[b][-1] = min
                bestH.append(homeTeam[b])
                homeTeam.pop(b)
            #get 7 best players for visitor team
            bestV = []
            for i in range(0,playersPerTeam):
                b = getBestPlayer(visitorTeam)
                min = visitorTeam[int(b)][-1]
                min = min.split(':')[0]
                visitorTeam[b][-1] = min
                bestV.append(visitorTeam[b])
                visitorTeam.pop(b)
            foo+=1
            #write game to csv
            writeCSV(game,g['spread'],g['home_score'],g['visitor_score'],g['home_id'],g['visitor_id'],homeTeamStats,visitorTeamStats,bestH,bestV,path,season,foo,beforeStreaks,home_history,visitor_history,home_history2,visitor_history2,home_history3,visitor_history3)


def formLastGame(data,team):
    print('forming last game data')
    print(team)
    if data is None:
        print('no data=---------=========------------==========')

    if data['data'][0]['game']['home_team_id'] == team:
        history_id = data['data'][0]['game']['home_team_id']
        opponent_id = data['data'][0]['game']['visitor_team_id']
        history_score = data['data'][0]['game']['home_team_score']
        opponent_score = data['data'][0]['game']['visitor_team_score']
    else:
        opponent_id = data['data'][0]['game']['home_team_id']
        history_id = data['data'][0]['game']['visitor_team_id']
        opponent_score = data['data'][0]['game']['home_team_score']
        history_score = data['data'][0]['game']['visitor_team_score']
    gameid = data['data'][0]['game']['id']

    opponent_players = []
    history_players = []
    
    for player in  data['data']:
        p = {}
        p['id'] = player['id']
        p['teamid'] = player['team']['id']
        print(player)
        for label in labels:
            if player['min'] is None:
                continue
            if label == 'min':
                min = player['min']
                min = min.split(':')[0]
                player['min']=min
            p[label] = player[label]
        if player['min'] is None:
            print('min is none------------')
            continue
        if p['teamid'] == history_id:
            history_players.append(p)
        if p['teamid'] == opponent_id:
            opponent_players.append(p)

    best_history_players = []
    best_opponent_players = []

    for i in range(0,5):
        best = historyBestPlayer(history_players)
        if best == '':
            break
        best_player = history_players.pop(int(best))
        best_history_players.append(best_player)


    for i in range(0,5):
        best = historyBestPlayer(opponent_players)
        if best == '':
            break
        best_player = opponent_players.pop(int(best))
        best_opponent_players.append(best_player)

    
    
    print('--------------------------------------------')
    return[best_history_players,best_opponent_players,history_score,opponent_score,gameid]


def historyBestPlayer(players):
    #print('players len ----------',len(players))
    best = ''
    topMin = 0
    for player in range(len(players)):
        min = players[player]['min']
        min = min.split(':')[0]
        #print(min,topMin)
        if min == '':
            continue
        if int(min) > int(topMin):
            best = player
            topMin = min
    return best


def writeCSV(game,spread, homeScore,visitorScore,homeId,visitorId,homeTeamStats,visitorTeamStats,bestH,bestV,path,season,foo,streaks,home_history,visitor_history,home_history2,visitor_history2,home_history3,visitor_history3):

    #form csv line
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

    line += ','+str(home_history[2])
    line += ','+str(home_history[3])
    line += ','+str(home_history[4])
    print(home_history[2],home_history[3],'--=-=-==-=-==-=-=--==-')
    for player in home_history[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in home_history[1]:
            for label in labels:
                line += ','+str(player[label])



    line += ','+str(visitor_history[2])
    line += ','+str(visitor_history[3])
    line += ','+str(visitor_history[4])
    print(visitor_history[2],visitor_history[3],'--=-=-==-=-==-=-=--==-')

    for player in visitor_history[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in visitor_history[1]:
            for label in labels:
                line += ','+str(player[label])



    line += ','+str(home_history2[2])
    line += ','+str(home_history2[3])
    line += ','+str(home_history2[4])
    print(home_history2[2],home_history2[3],'--=-=-==-=-==-=-=--==-')
    for player in home_history2[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in home_history2[1]:
            for label in labels:
                line += ','+str(player[label])



    line += ','+str(visitor_history2[2])
    line += ','+str(visitor_history2[3])
    line += ','+str(visitor_history2[4])
    print(visitor_history2[2],visitor_history2[3],'--=-=-==-=-==-=-=--==-')

    for player in visitor_history2[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in visitor_history2[1]:
            for label in labels:
                line += ','+str(player[label])

    '''





    line += ','+str(home_history3[2])
    line += ','+str(home_history3[3])
    line += ','+str(home_history3[4])
    print(home_history3[2],home_history3[3],'--=-=-==-=-==-=-=--==-')
    for player in home_history3[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in home_history3[1]:
            for label in labels:
                line += ','+str(player[label])



    line += ','+str(visitor_history3[2])
    line += ','+str(visitor_history3[3])
    line += ','+str(visitor_history3[4])
    print(visitor_history3[2],visitor_history3[3],'--=-=-==-=-==-=-=--==-')

    for player in visitor_history3[0]:
            for label in labels:
                line += ','+str(player[label])
    for player in visitor_history3[1]:
            for label in labels:
                line += ','+str(player[label])



    '''

    if len(visitor_history[0])<=4 or len(visitor_history[1])<=4 or len(home_history[0])<=4 or len(home_history[1]) <=4:
        return
    #use 2022 games as test for evaluation
    random_number = random.randint(0, 100)

     #use 2022 games as test for evaluation
    random_boolean = random.choice([True, False])

    if season == '2022' or season == '2021':
        if random_boolean:#sets split of test/train on final season.....
            csv = open('csv/test.csv','a')
            csv.write(line+'\n')
            return ''

    csv = open(path,'a')
    csv.write(line+'\n')
    #print(line)

#write csv header
def writeCSVHeader(labels, path,**kwargs):
    header = 'home_score,visitor_score,gameid,spread,home_id,home_streak,hgp,hw,hl,visitor_id,visitor_streak,vgp,vw,vl'
    derp = ['home_', 'visitor_']
    for foo in derp:#iterate home/visitor
        for i in range(0,playersPerTeam):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label

    header+=',home_history_score,home_opponent_history_score,home_history_gameid'
    derp = ['home_history_', 'home_opponent_history_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label
    header+=',visitor_history_score,visitor_opponent_history_score,visitor_history_gameid'
    derp = ['visitor_history_', 'visitor_opponent_history_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label



    header+=',home_history2_score,home_opponent_history2_score,home_history2_gameid'
    derp = ['home_history2_', 'home_opponent_history2_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label
    header+=',visitor_history2_score,visitor_opponent_history2_score,visitor_history2_gameid'
    derp = ['visitor_history2_', 'visitor_opponent_history2_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label

    '''

    
    header+=',home_history3_score,home_opponent_history3_score,home_history3_gameid'
    derp = ['home_history3_', 'home_opponent_history3_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label
    header+=',visitor_history3_score,visitor_opponent_history3_score,visitor_history3_gameid'
    derp = ['visitor_history3_', 'visitor_opponent_history3_']
    for foo in derp:#iterate home/visitor
        for i in range(0,5):#iterate players
            for label in labels:#iterate stat labels
                header+=','+foo+str(i)+'_'+label

    '''

    csv = open(path,'w')#write train
    csv.write(header+'\n')
    csv = open('csv/test.csv','w')#write test
    csv.write(header+'\n')
    return header



#gets best player on team
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
    # Adjusted to parse the full date-time string
    return sorted(games, key=lambda game_id: datetime.strptime(games[game_id]['date'], '%Y-%m-%dT%H:%M:%S.%fZ'))



#save pkl object
def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#load pkl object
def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


#request api
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
 
#get season average
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


main(labels,seasons)


