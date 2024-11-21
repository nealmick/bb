import requests, json, time, operator, pickle, random



url = 'https://www.balldontlie.io/api/v1/'
seasons = ['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005']
seasons.reverse()
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min
createPlayersByTeam = False
loadIds=True#load saved unigameid or fetch new.... used in getGameIds()

def main(seasons,labels,url):
    

        season = '2022'
        print("season"+season)
        try:
            SeasonAverages = load_obj(season+'SeasonAverages')
        except FileNotFoundError:
            SeasonAverages = {}
        playersByTeam = load_obj(season+'playerIdByTeamID')
        playerIds = combinePlayerIds(playersByTeam)

        for playerId in playerIds:
            if playerId not in SeasonAverages:
                seasonAverage = getSeaonAverage(playerId,season,labels)
                SeasonAverages.update({playerId:seasonAverage})
                print(len(SeasonAverages))
            save_obj(SeasonAverages,season+'SeasonAverages')
        #getPlayersByGameID(createPlayersByTeam,data,season,url)


#returns game info
def getGame(gameid,season):
    print("Get Game")
    url = 'https://www.balldontlie.io/api/v1/stats?seasons[]='+str(season)
    url +='&game_ids[]='+str(gameid)

    r = req(url)
    response = r
    if not r['data']:
        return False
    r = r['data'][0]
    if r['game']['home_team_score'] > r['game']['visitor_team_score']:
        w = 1
    else:
        w = 0 
    return {
    'winner':1,
    'date': r['game']['date'],
    'home_id':r['game']['home_team_id'],
    'home_score':r['game']['home_team_score'],
    'visitor_id':r['game']['visitor_team_id'],
    'visitor_score':r['game']['visitor_team_score'],
    'data' : response['data']
    }

def getWinner(gameid,season):

    url = 'https://www.balldontlie.io/api/v1/stats?seasons[]='+str(season)
    url +='&game_ids[]='+str(gameid)
    r = req(url)
    if not r['data']:
        return False
    r = r['data'][0]
    if r['game']['home_team_score'] > r['game']['visitor_team_score']:
        return {'winner':1,'home':r['game']['home_team_id'],'visitor':r['game']['visitor_team_id']}
    else:
        return {'winner':0,'home':r['game']['home_team_id'],'visitor':r['game']['visitor_team_id']}

def getSeaonAverage(playerId,season,labels):
    url = 'https://www.balldontlie.io/api/v1/season_averages?season='+season
    url+='&player_ids[]='+str(playerId)
    r = req(url)
    if len(r['data'])==0:
        print('no season average-----------------')
        return []
    r = r['data'][0]
    seasonAverage = []
    for label in labels:
        seasonAverage.append(r[label])
    return seasonAverage
def combinePlayerIds(playersByTeam):
    playerIds = []
    for team in playersByTeam:
        
        for player in playersByTeam[team]:
            playerIds.append(player)
    return playerIds
        

def getGameIds(season,**kwargs):
    if loadIds:
        gameids = load_obj(season+'uniGameIds')
    else:
        gameids = uniGameIDs(season)#returns all unique game ids for the season
        save_obj(gameids, season+'uniGameIds')
    return gameids
#takes season returns list of unique game ids
def uniGameIDs(season):
    gameids = []
    #start by getting all the team ids...
    for teamid in range(1,31):#30 teams in nba
        getGameIDByTeam(season, teamid, gameids)
    for game in range(len(gameids)):#iterate games
        if gameids.count(game) > 1:#check if any dups
            del gameids[game]#delete dups
    return gameids
#gets game ids by season and team....
def getGameIDByTeam(season, teamid, gameids):
    url = 'https://www.balldontlie.io/api/v1/games?seasons[]='
    url += season + '&team_ids[]=' + str(teamid)
    response = req(url)
    url+='&page='
    found = True
    for page in range(1,response['meta']['total_pages']+1):
        response = req(url+str(page))
        for game in range(len(response['data'])):
            if found:
                gameids.append(response['data'][game]['id'])
    return gameids
#----------------------

def getPlayersByGameID(count,gameid,season,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/stats?seasons[]='+str(season)
    url +='&game_ids[]='+str(gameid)
    response = req(url)#need this requesst to get total_pages
    #iterate through pages
    playersByTeam = load_obj(season+'PlayerIdByTeamID')
    foundNew=False

    for player in range(0,len(response['data'])):

        playerTeamId=response['data'][player]['player']['team_id']#set the team id of the player
        id=response['data'][player]['player']['id']
        if id not in playersByTeam[str(playerTeamId)]:
            print("found new")
            foundNew=True
            playersByTeam[str(playerTeamId)].append(id)


    save_obj(playersByTeam, season+'PlayerIdByTeamID')
    
    if not foundNew:
        count = count+1
    if foundNew:
        count = 0
    return count


def createPlayersByTeam(season):
    playersByTeam = {}
    for i in range(0,31):
        playersByTeam.update({str(i):[]})
    save_obj(playersByTeam, season+'PlayerIdByTeamID')


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

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


main(seasons,labels,url)




'''
    collectGames(seasons,labels,url)




    #collect's game info
    def collectGames(seasons,labels,url):
        for season in seasons:
                gameids = getGameIds(season)
                try:
                    games = load_obj(season+'Games')
                except FileNotFoundError:
                    games = {}
                games = {}
                print(games)
                for id in gameids:
                    #if id not in winnersById:
                    game = getGame(id,season)

                    if game:
                        games.update({id:game})
                        save_obj(games, season+'Games')
                        print(id, games[id]['winner'],games[id]['date'],games[id]['home_id'],games[id]['home_score'],games[id]['visitor_id'],games[id]['visitor_score'])
                        print(len(games[id]['data']))






 print("season"+season)
        try:
            SeasonAverages = load_obj(season+'SeasonAverages')
        except FileNotFoundError:
            SeasonAverages = {}
        playersByTeam = load_obj(season+'playerIdByTeamID')
        playerIds = combinePlayerIds(playersByTeam)

        for playerId in playerIds:
            if playerId not in SeasonAverages:
                seasonAverage = getSeaonAverage(playerId,season,labels)
                SeasonAverages.update({playerId:seasonAverage})
                print(len(SeasonAverages))
            save_obj(SeasonAverages,season+'SeasonAverages')
        #getPlayersByGameID(createPlayersByTeam,data,season,url)





        gameids = getGameIds(season)#gets game ids either from saved if loadids =true or calls get uniGameIDs to get fresh game ids that r uni
        count = 0
        while True:
            gameid = random.choice(gameids)
            count = getPlayersByGameID(count,gameid, season)
            playersByTeam = load_obj(season+'PlayerIdByTeamID')
            s = ''
            for team in playersByTeam:
                s= s+' '+str(len(playersByTeam[team]))
            print(s)
            print(count)
            if count >=10:
                break



'''
