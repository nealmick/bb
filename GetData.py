

import requests, json, time, operator, pickle, random

#seasons = ['2012','2006','2005','2004','2003','2002','2001','2000']
season = '2019'#nba season#dis b 4 dah future games cuh
#stat labels
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min
#path = season+'test.csv'#path used for csv
path = season+'update.csv'
skipToGameID = 0#for debug if there is problem...# otherwise leave 0
loadIds = False#set true false if u want load saved gameids..#set false if you wanna like wana create new save file, it will then be set true after first run#im tired
loadPlayerStats = False#set true false if u want to load saved playerstats
createCSV = True#red alerater this will overrite data if set to true #new csv will be ceeated or written over old...
createPlayersByTeam = True#creates pkl file for player ids stored by teamid.....
futureGameLoad = False#creates pkl file for player ids stored by teamid.....
#for future game:
date='2020-2-29'
homeAbv='BOS'
visitorAbv='HOU'

#--------------------------#
def main(loadPlayerStats,createPlayersByTeam, **kwargs):
    gameids = getGameIds()#gets game ids either from saved if loadids =true or calls get uniGameIDs to get fresh game ids that r uni
    if createCSV:
        writeCSVHeader(labels, path)
    if skipToGameID != 0:
        found = False
    else:
        found=True
    for gameid in gameids:#iterate through all games returned by uniGameIDs
        if found:
            data = nextGame(gameid)#retsets data and sets the game id....
            createPlayersByTeam,data = getPlayersByGameID(createPlayersByTeam, data)#gets player ids by game ids
            if data['gameid'] != 'tooFewPlayers':
                loadPlayerStats = getPlayerAvg(data, loadPlayerStats)#gets players stats by player ids
                minuteConversion(data)#chops off seconds se we only have mins
                sortByPlayTime(data)#sorts player into two groups good players and team players
                #avgTeamPlayers(data)#returns the average of team players stats as one single player call avg
                #printStats(data,True)
                writeCSV(data, path)
        if gameid == skipToGameID:
            found = True
#--------------------------#

#gets futegame
def futureGame(date,homeAbv,visitorAbv,path,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    url+=date
    response = req(url)
    nOsTAtsYET = {}
    for game in range(len(response['data'])):
        if response['data'][game]['home_team']['abbreviation']==homeAbv and response['data'][game]['visitor_team']['abbreviation']==visitorAbv:
            gameid = response['data'][game]['id']
            data = nextGame(gameid)
            data.update({'home_team_id':response['data'][game]['home_team']['id']})
            data.update({'visitor_team_id':response['data'][game]['visitor_team']['id']})
            playerIdByTeamID = load_obj('2019PlayerIdByTeamID')
            for player in playerIdByTeamID[str(data['home_team_id'])]:
                data['home_team_players'].update({ player : nOsTAtsYET})
            for player in playerIdByTeamID[str(data['visitor_team_id'])]:
                data['visitor_team_players'].update({ player : nOsTAtsYET})
            data.update({'home_team_score' : response['data'][game]['home_team_score']})
            data.update({'visitor_team_score' : response['data'][game]['home_team_score']})
            getPlayerAvg(data, loadPlayerStats)#gets players stats by player ids
            minuteConversion(data)#chops off seconds se we only have mins
            sortByPlayTime(data)#sorts player into two groups good players and team players
            writeCSVHeader(labels, path)
            writeCSV(data, path)
#single game of past
def singleGame(gameid,path,**kwargs):
    writeCSVHeader(labels, path)
    data = nextGame(gameid)
    getPlayersByGameID(data)
    if data['gameid']!='tooFewPlayers':#singgame non future
        getPlayerAvg(loadPlayerStats, data)
        minuteConversion(data)
        sortByPlayTime(data)
        writeCSV(data, path)


def writeCSV(data, path, **kwargs):
    derp = ['home', 'visitor']
    if data['home_team_score']>=data['visitor_team_score']:
        line = '1'
    else:
        line = '0'
    if data['gameid'] != 'tooFewPlayers':
        print('writing----------------------------------')
        line+=','+str(data['gameid'])
        for foo in derp:
            for goodPlayer in data[foo+'_good_players']:
                for label in labels:
                    line+=','+str(data[foo+'_good_players'][goodPlayer][label])
            #for averages
            #for label in labels:
                #line+=','+str(data[foo+'_team_players']['avg'][label])
        c = line.count(',')
        #if c == 229:
        csv = open(path,'a')#appending
        csv.write(line+'\n')
        #else:
            #print('+++++##########RED ALERT SUMTHING WENT WRONG AND MADE IT PAST ALL CHECKS FFS')
    else:
        print('gameid: -------------',data['gameid'],len(data['home_team_players']))
        print('gameid: -------------',data['gameid'],len(data['visitor_team_players']))

#------------------------
def printStats(data, avg, *kwargs):
    print('stats:')
    derp = ['home', 'visitor']
    for foo in derp:
        for player in data[foo+'_good_players']:
            print('player id-----------: ', player)
            for label in labels:
                print(label, ' : ', data[foo+'_good_players'][player][label])
        if avg:
            print('num of extra players avg: ',len(data[foo+'_team_players']))
            for label in labels:
                print(foo,' avg ',label, ' : ', data[foo+'_team_players']['avg'][label])
            print('season for good measures ', data[foo+'_team_players']['avg']['season'])#this will show if sumtin messed up in the avg faze lol fazeClan mlg pro 360 no scope
#------------------------
def avgTeamPlayers(data, **kwargs):
    derp = ['home', 'visitor']
    temp = {}
    temp.update({'avg':{}})#gona be a double dict
    for foo in derp:
        data[foo+'_team_players'].update({'avg' : {}})
        first = True
        count = -1#this is correct, i verified by look at season and it indeed makes season correct again
        for player in data[foo+'_team_players']:
            count += 1
            for statName in data[foo+'_team_players'][player]:
                if first:
                    temp['avg'].update({statName : data[foo+'_team_players'][player][statName]})
                else:
                    temp['avg'].update({statName: temp['avg'][statName]+data[foo+'_team_players'][player][statName]})
            first = False
        for statName in temp['avg']:
            if count > 0:#toofewplayers....
                data[foo+'_team_players']['avg'].update({statName:int(temp['avg'][statName])/count})
            else:
                data.update({'gameid' : 'tooFewPlayers'})
    return data
#--------------------------#
def sortByPlayTime(data):
    derp = ['home', 'visitor']
    for foo in derp:
        for i in range(3):
            maxMin = 0
            id = ''
            for player in data[foo+'_team_players']:
                old = maxMin
                maxMin = max(maxMin, int(data[foo+'_team_players'][player]['min']))
                if maxMin > old:#this line messed me up i had >= and could figure out why it wasnt working finally got it.
                    id = player
            try:
                data[foo+'_good_players'].update({id : data[foo+'_team_players'][id]})
                data[foo+'_team_players'].pop(int(id), None)
            except KeyError:
                print('key error')
    return data

#--------------------------#
def printPlayerTime(data):
    derp = ['home', 'visitor']
    for foo in derp:
        for player in data[foo+'_team_players']:
            print(data[foo+'_team_players'][player]['min'])
#--------------------------#
def minuteConversion(data):
    #chop seconds off...
    derp = ['home', 'visitor']
    for foo in derp:#iter home visitor
        for player in data[foo+'_team_players']:#iter players
            min = ''
            if data[foo+'_team_players'][player] != '':#takes care of non values
                time = data[foo+'_team_players'][player]['min']
                if str(type(time)) == "<class 'str'>":
                    for char in time:#iter charecters in time
                        if char != ':':
                            min += str(char)
                        else:
                            break
                    data[foo+'_team_players'][player].update({'min' : min})
                        #print(data[foo+'_team_players'][player]['min'])
    return data

#--------------------------#
#gets season average stats by player ids.....
def getPlayerAvg(data, loadPlayerStats,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/season_averages?season='
    url += season+'&player_ids[]='
    teams = ['home', 'visitor']
    if loadPlayerStats:
        playerStats = load_obj(season+'playerStats')
        print('loaded # player stats: ', len(playerStats))
    else:
        loadPlayerStats = True
        playerStats = {}
    for team in teams:
        badPlayer = False
        badPlayerid = 0#gosh i hope there is only ever 1 of these on each team else smh nooo
        for playerid in data[team+'_team_players']:
            foundSaved = False
            #check if player has been saved
            for splayerid in playerStats:
                if playerid == splayerid:
                        data[team+'_team_players'].update({playerid : {}})#here it is again#soo anoying
                        for statName in playerStats[playerid]:
                            data[team+'_team_players'][playerid].update({statName :playerStats[playerid][statName]})
                        print('found saved -----------####-------------id: ', playerid)
                        foundSaved = True
                        break
            #get unsaved season averages
            if not foundSaved:
                uurl = url+str(playerid)
                response = req(uurl)
                #wtf ig it was setting all playerids to the same then laying the stats down its fucked tho this pissed me off soo fucking much
                data[team+'_team_players'].update({playerid : {}})#this fucking line holly fuck took me 3 hours to figure out why all the stas where the same
                print(len(response['data']))
                if len(response['data']) != 0:#this is sad it means a player didnt play a single game all season lmao poor player
                    for statName in response['data'][0]:
                        data[team+'_team_players'][playerid].update({ statName: response['data'][0][statName]})
                    playerStats.update({playerid : {}})
                    for statName in data[team+'_team_players'][playerid]:
                        playerStats[playerid].update({statName : data[team+'_team_players'][playerid][statName]})
                    print('not saved -----------####-------------id: ', playerid)
                else:
                    badPlayer = True
                    badPlayerid = playerid
        if badPlayer:
            print('badplayer#--------', badPlayerid)
            data[team+'_team_players'].pop(badPlayerid, None)
            badPlayer=False

    save_obj(playerStats, season+'playerStats')
    return loadPlayerStats, data

#--------------------------#
#takes data gets gameid and update data with all the player ids
def getPlayersByGameID(createPlayersByTeam, data,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/stats?seasons[]='+str(season)
    url +='&game_ids[]='+str(data['gameid'])
    response = req(url)#need this requesst to get total_pages
    setScore(response, data)
    nOsTAtsYET = {}
    #iterate through pages
    if not createPlayersByTeam:
        playersByTeam = load_obj(season+'PlayerIdByTeamID')
        print('loaded=============')
    if createPlayersByTeam:
        print('============')
        playersByTeam = {}
        for i in range(0,31):
            playersByTeam.update({str(i):[]})
    h =[]
    v =[]
    homeTeamId = 0
    visitorTeamId = 0
    for page in range(1, response['meta']['total_pages']+1):
        response = req(url+'&page='+str(page))
        for player in range(0,len(response['data'])):
            try:
                try:
                    #print(type(response['data'][player]['player']['team_id']))
                    #if response['data'][player]['player']['team_id'] != None:
                    playerTeamId=response['data'][player]['player']['team_id']#set the team id of the player
                    #set the otherids.... and check which is the player....
                    homeTeamId=response['data'][player]['game']['home_team_id']
                    visitorTeamId=response['data'][player]['game']['visitor_team_id']
                    id=0
                    if playerTeamId == homeTeamId:
                        id=response['data'][player]['player']['id']
                        data['home_team_players'].update({ id : nOsTAtsYET})#lolcap
                        h.append(id)
                    if playerTeamId == visitorTeamId:
                        id=response['data'][player]['player']['id']
                        data['visitor_team_players'].update({ id: nOsTAtsYET})
                        v.append(id)
                except KeyError as e:
                    print(e)
            except TypeError as e:
                print(e)
    a = [homeTeamId, homeTeamId]
    for team in a:
        all = []
        for playerid in playersByTeam[str(team)]:
            all.append(playerid)
        if team == homeTeamId:
            for playerid in h:
                all.append(playerid)
        if team == visitorTeamId:
            for playerid in v:
                all.append(playerid)
        playersByTeam.update({str(team):all})
    print(playersByTeam)
    save_obj(playersByTeam, season+'PlayerIdByTeamID')
    data = checkPlayerAmount(data)
    createPlayersByTeam=False
    return createPlayersByTeam, data
#--------------------------#
#checks to make sure we have atleast 8 player ids...
def checkPlayerAmount(data):
    teams =['home','visitor']
    for team in teams:
        if len(data[team+'_team_players']) <3:
            print('tooFewPlayers------------',len(data[team+'_team_players']))
            data.update({'gameid' : 'tooFewPlayers'})
    return data

#sets score for both teams
def setScore(response, data):
    if response['meta']['total_pages'] > 0:
        teams = ['home','visitor']
        for team in teams:
            data.update({team+'_team_score' : response['data'][0]['game'][team+'_team_score']})
        return data
#--------------------------#
#will either load save game ids or start to retrieve them by season...
def getGameIds(**kwargs):
    if loadIds:
        gameids = load_obj(season+'uniGameIds')
    else:
        gameids = uniGameIDs(season)#returns all unique game ids for the season
        save_obj(gameids, season+'uniGameIds')
    return gameids
#--------------------------#
#clears data of last game and gets ready for next
def nextGame(gameid):
    data = {}
    data.update({'gameid' : gameid})
    data.update({'home_team_players' : {}})
    data.update({'visitor_team_players' : {}})
    data.update({'home_good_players' : {}})
    data.update({'visitor_good_players' : {}})
    #data.update({'home_team_id' : 0})
    #data.update({'visitor_team_id' : 0})

    return data
#--------------------------#
#takes season returns list of unique game ids
def uniGameIDs(season):
    gameids = []
    #start by getting all the team ids...
    for teamid in range(1,31):#30 teams in nba
        getGameIDByTeam(season, teamid, gameids)
    for game in range(len(gameids)):#iterate games
        if gameids.count(game) > 1:#check if any dups
            del gameid[game]#delete dups
    return gameids
#--------------------------#
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

#--------------------------#
def writeCSVHeader(labels, path):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(1,4):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    return header
#--------------------------#
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
#--------------------------#
def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#--------------------------#
'''
gameid = 63439
path = 'single.csv'
singleGame(gameid,path)
'''

if not futureGameLoad:
    main(loadPlayerStats,createPlayersByTeam)
if futureGameLoad:
    futureGame(date, homeAbv,visitorAbv,path)
##-----------------------##
