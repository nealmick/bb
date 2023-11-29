from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
from pytz import timezone
import webData
import webTrain
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponsePermanentRedirect
from .models import Game
from users.models import Profile, Message


from tensorflow.keras import *
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import tensorflow as tf


import requests, json, time, operator, pickle, random,os,shutil
import functools
import numpy as np
import pandas as pd
import csv

#stats for season averages
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
#number of top players input for each game
playersPerTeam = 7

ABV = [
    'ATL',
    'BKN',
    'BOS',
    'CHA',
    'CHI',
    'CLE',
    'DAL',
    'DEN',
    'DET',
    'GSW',
    'HOU',
    'IND',
    'LAC',
    'LAL',
    'MEM',
    'MIA',
    'MIL',
    'MIN',
    'NOP',
    'NYK',
    'OKC',
    'ORL',
    'PHI',
    'PHX',
    'POR',
    'SAC',
    'SAS',
    'TOR',
    'UTA',
    'WAS',
]

TEAMCOLORS = {
    'ATL':'#E03A3E',
    'BKN':'#000000',
    'BOS':'#158248',
    'CHA':'#1B6D87',
    'CHI':'#CE1341',
    'CLE':'#FAB81C',
    'DAL':'#287DC5',
    'DEN':'#FBC627',
    'DET':'#DD1631',
    'GSW':'#236BB6',
    'HOU':'#CE1341',
    'IND':'#FABB30',
    'LAC':'#2F7ABC',
    'LAL':'#552583',
    'MEM':'#6189B9',
    'MIA':'#980B2E',
    'MIL':'#06471A',
    'MIN':'#236192',
    'NOP':'#E31837',
    'NYK':'#236BB6',
    'OKC':'#F05134',
    'ORL':'#2677BD',
    'PHI':'#236BB5',
    'PHX':'#F9A01B',
    'POR':'#C6122A',
    'SAC':'#5A2D81',
    'SAS':'#1c1c1c',
    'TOR':'#CD1341',
    'UTA':'#FAA403',
    'WAS':'#CF142C',
}



#clear user's profile stats in order to reset account...
def clearStats(request):
    #dont clear stats for demo user
    if request.user == 'demo':
        return redirect('home-predict')
    #load profile object
    obj = Profile.objects.filter(user=request.user)
    #reset profile stats
    obj.update(correct=0)
    obj.update(predictions=0)
    obj.update(loss=0)
    obj.update(gain=0)
    obj.update(ev_won=0)

    obj.update(ev_margin1=0)
    obj.update(ev_margin2=0)
    obj.update(ev_margin3=0)
    obj.update(ev_won_count=0)
    obj.update(ev_margin1_count=0)
    obj.update(ev_margin2_count=0)
    obj.update(ev_margin3_count=0)

    return redirect('home-predict')

#Delete all games
#this delete's Game model instances, and does not delete csv game files
#might be a good idea to delete csv files in future if there gets to be alot...
def clearGames(request):
    #block demo from clearing games
    if request.user == 'demo':
        return redirect('home-predict')
    #delete all game objects with author request.user
    Game.objects.filter(author=request.user).delete()
    return redirect('home-predict')

## renders confirm clear template for account reset.
def confirmClearGames(request):
    return render(request,'predict/confirm.html')

#Updates spread table at bottom of edit game view
#this does not update spread at top displayed draftking/fanduel
#maybe work on that in future
def updateSpread(request, pk):
    #get game obj from pk
    g = Game.objects.filter(pk=pk)
    #get home and visitor abv with game date
    home = g.values('home')[0]['home']
    visitor = g.values('visitor')[0]['visitor']
    date = g.values('gamedate')[0]['gamedate']
    #request spread
    spread = getSpread(home,visitor,date)
    #set new spread
    complexSpread = spread[2]
    complexSpread=json.dumps(complexSpread)
    g.update(complexSpread=complexSpread)
    #redirect back to game
    return redirect('edit-predict',pk)

# Bet list view
# calculates time series data, and can be filtered for teams
def betsList(request,team=None, days=30):
    context = {}
    g = Game.objects.filter(author=request.user)
    g = g.filter(bet=True)
    g = g.filter(finished=True)
    print(team)
    if team != 'all' and team is not None:
        print('filtering for team',team)
        context['filter'] = team
        g = g.filter(Q(home=team) | Q(visitor=team))
    else:
        context['filter'] = 'all'
    g = g.order_by('-gameid')
    count = 0
    total= 0
    
    history = []
    last = 0


    historyTotal = 0

    for day in range(days,0,-1):
        history.append(historyTotal)
        print(day)
        foo = datetime.now() - timedelta(days=day)
        print(foo)
        for game in g:
            d = datetime.strptime(game.gamedate, '%Y-%m-%d')
            if foo.strftime('%Y-%m-%d') == d.strftime('%Y-%m-%d'):
                if game.ev_won == '1':
                    historyTotal+=90.1
                else:
                    historyTotal-=100
    foo = datetime.now()
    c = 0
    cut = 0
    for game in g:
        c+=1
        d = datetime.strptime(game.gamedate, '%Y-%m-%d')
        d = str(foo - d).split(' ')[0]
        if int(d) >= days:
            cut = c
            break
        
        if game.ev_won == '1':
            count+=1
            total+=90.1
        else:
            total-=100

    if c>1:
        g = g[0:c-1]
    print(len(g),c)
    h = json.dumps(history)
    context['history'] = h
    context['numBets'] = len(g)
    context['correct'] = count
    context['wrong'] = len(g)-count
    context['totalSpent'] = len(g)*100
    context['totalWon'] = count*190
    context['totalProfit'] = count*190-len(g)*100
    context['total'] = total
    context['maxSpent'] = round(min(history))
    context['maxWon'] = round(max(history))
    try:
        context['p'] = round(count/len(g)*100)
    except ZeroDivisionError:
        context['p'] = 0
    context['games'] = g
    context['abv'] = ABV
    context['days'] = days
    return render(request,'predict/bets.html',context)



#Sets game bet true/false
def setBet(request, pk):
    g = Game.objects.filter(pk=pk)
    bet = g.values('bet')[0]['bet']
    if bet:#is bet already true?
        g.update(bet=False)
    else:#if not set true
        g.update(bet=True)
    return redirect('edit-predict', pk)#redirect back to game

# all 30 teams list view
# then added the search view at top and repurposed into a general data view
def teamListView(request):
    context={}

    #load team data
    teamNamesbyID = load_obj('teamNamesbyID')
    teamAbvById = load_obj('teamAbvById')
    teamId = 0
    teams = []
    #iterate over teams prepare data.....
    for id in teamNamesbyID:
        team = {}
        team['id'] = id
        team['name'] = teamNamesbyID[int(id)]
        team['abv'] = teamAbvById[int(id)]
        stats = getTeamData(team['abv'],team['abv'])
        stats = stats[0]
        win = stats[1]
        loss = stats[2]
        streak = stats[3]
        team['win'] = win
        team['loss'] = loss
        team['streak'] = streak
        teams.append(team)#append team to teams object

    context['teams'] = teams#main teams context obj
    return render(request,'predict/teamList.html',context)


# Team detail page
# Displays teams current status, with the full rosters in no particular order
def teamView(request,abv):
    abv = abv.upper()#make team abv upper case
    context={}
    #load data
    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    teamNamesbyID = load_obj('teamNamesbyID')
    teamAbvById = load_obj('teamAbvById')
    teamId = 0
    #get team id
    for id in teamAbvById:
        if teamAbvById[id] == abv:
            teamId=id
    context['teamId'] = teamId#set team id
    teamName = teamNamesbyID[int(teamId)]#team full name
    players = playerIdByTeamID[str(teamId)]#team roster of players
    p = []
    #iterate over players get player name
    for player in players:
        foo = {}
        try:
            foo['name'] = obj[str(player)]
        except KeyError:
            try:
                foo['name'] = obj[int(player)]
            except KeyError:
                url = 'https://www.balldontlie.io/api/v1/players/'
                r = req(url+str(player))
                fn = r['first_name']
                ln = r['last_name']
                full = fn+' '+ln
                obj.update({str(player) : full})
                save_obj(obj,'2019PlayerNamesByID')
                foo['name'] = full
        #get player season average
        foo['avg'] = seasonAverages[player]
        foo['id'] = player
        data = getPlayerInfo(abv,foo['name'])
        foo['data'] = data
        p.append(foo)#append foo player p players


    context['p'] = p

    context['labels'] = labels




    #get team data and set context data
    stats = getTeamData(abv,abv)
    stats = stats[0]
    win = stats[1]
    loss = stats[2]
    streak = stats[3]
    context['team'] = teamName
    context['abv'] = abv
    context['win'] = win
    context['loss'] = loss
    context['streak'] = streak

    return render(request,'predict/team.html',context)



# Takes player id as input, request current team from api, then compares with saved roster
# if savedId != updatedId the player will be removed from old team and added to new.
def updatePlayerTeam(request,playerId,**kwargs):
    print('updating team')
    #request api for new team id
    url = 'https://www.balldontlie.io/api/v1/players/' + str(playerId)
    r = req(url)
    updatedId=str(r['team']['id'])#set updated id
    savedId=0
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')#get current rosters
    for team in playerIdByTeamID:#get team
        count=0
        for id in playerIdByTeamID[team]:
            if str(playerId) == str(id):#get player in team
                savedId = team#saved team id
                if int(savedId) != int(updatedId):#is saved id different then updated id
                    print('remove index:',count)
                    playerIdByTeamID[team].pop(count)#remove from old team
                    playerIdByTeamID[updatedId].append(playerId)# add to new team
            count+=1
    
    save_obj(playerIdByTeamID,'2022PlayerIdByTeamID')#save obj
    print('saved team id:',savedId)
    print('updated team id:',updatedId)
    #redirect back to player
    return redirect('player-detail',playerId)

# takes player api id, Request new season averages
# then loads season averages object and updates the player stats
def updatePlayerStats(request,playerId,**kwargs):
    print('updating stats')
    seasonAverages = load_obj('2022SeasonAverages')#load saved stats
    #request api for new stats
    url='https://www.balldontlie.io/api/v1/season_averages?player_ids[]='+str(playerId)
    r=req(url)
    res = []
    for label in labels:
        try:
            res.append(r['data'][0][label])#create new data obj
        except IndexError:
            return redirect('player-detail',playerId)

    seasonAverages[playerId] = res#update player stats with new obj
    print(seasonAverages[playerId])
    save_obj(seasonAverages,'2022SeasonAverages')#save obj
    #redirect back to player
    return redirect('player-detail',playerId)

# Used by player search result to convert results of a player name to player id
# takes player name or Key and redirects to player detail of id
def playerDetailbyName(request,key):
    obj = load_obj('2019PlayerNamesByID')#load saved player names by id
    player_id =''
    for id in obj:#look for player id
        if obj[id].replace("'", "-") == key:#convert ' apostrophe with - dash
            print(id)
            player_id = id#found player id
            break
    #redirect player detail page of player id
    return redirect('player-detail', player_id)
    

# Player detail view shows ESPN image, current stats, and status.
# takes player API ID
def playerDetail(request,playerId):
    context={}
    context['id'] = playerId
    context['labels'] = labels
    #requesting api for updated player info
    url = 'https://www.balldontlie.io/api/v1/players/' + str(playerId)
    r = req(url)
    #setting context from request
    context['weight_pounds'] = r['weight_pounds']
    context['height_feet'] = r['height_feet']
    context['height_inches'] = r['height_inches']
    context['position'] = r['position']
    context['conference'] = r['team']['conference']
    context['division'] = r['team']['division']
    context['abv'] = r['team']['abbreviation']
    #load saved objects
    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    teamNamesbyID = load_obj('teamNamesbyID')
    #set plater name
    try:
        context['name'] = obj[str(playerId)]
    except KeyError:
        context['name'] = obj[int(playerId)]
        print('e')
    #set season average
    context['seasonAverage'] = seasonAverages[playerId]
    context['team'] = 0
    #get team
    for team in playerIdByTeamID:
        for id in playerIdByTeamID[team]:

            if str(playerId) == str(id):
                context['team'] = team
                context['team_name'] = teamNamesbyID[int(team)]



    #get player api data
    data = getPlayerInfo(context['abv'],context['name'])
    context['data']=data
    #render detail page
    return render(request,'predict/playerDetail.html',context)


# called in playerDetail to request individual player details
# takes team abv and player name, returns data['espnLink'] etc....
def getPlayerInfo(team,playerName):
    #convert team abv, there are some that dont match...
    convert = {
        'ATL' : 'ATL',
        'BKN':  'BKN',
        'BOS':  'BOS',
        'CHA':  'CHA',
        'CHI':  'CHI',
        'CLE':  'CLE',
        'DAL':  'DAL',
        'DEN':  'DEN',
        'DET':  'DET',
        'GSW':  'GS',
        'HOU':  'HOU',
        'IND':  'IND',
        'LAC':  'LAC',
        'LAL':  'LAL',
        'MEM':  'MEM',
        'MIA':  'MIA',
        'MIL':  'MIL',
        'MIN':  'MIN',
        'NOP':  'NO',
        'NYK':  'NY',
        'OKC':  'OKC',
        'ORL':  'ORL',
        'PHI':  'PHI',
        'PHX':  'PHO',
        'POR':  'POR',
        'SAC':  'SAC',
        'SAS':  'SA',
        'TOR':  'TOR',
        'UTA':  'UTA',
        'WAS':  'WAS',
        }
    
    t=convert[team]
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBATeams"

    querystring = {"schedules":"true","rosters":"true"}


    key = 'c25bdc2c24msh8b9b73d7c986ea0p1a2cc1jsn7aaf7636b342'
    
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }
    seconds = 0
    teamStats = load_obj('teamStats')
    response = []
    #check if we have saved request within 1800 seconds, if so dont request again
    #this is the team data caching system...
    try:
        lastupdate = teamStats['lastupdate']
        now = datetime.now()
        time_diff = now-lastupdate
        seconds = time_diff.total_seconds()
        print('Seconds since last update',seconds)
    except KeyError:
        print('no saved team stats found')
        teamStats = {}
    if seconds == 0 or seconds>1800:
        print('getting updated results')
        #didnt find cache make request
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        lastupdate = datetime.now()
        teamStats['response']=response
        teamStats['lastupdate']=lastupdate
        save_obj(teamStats,'teamStats')
    else:
        print('loaded cached results')
        response = teamStats['response']

    r = response['body']
    data = {}
    #iterate through api response 
    for team in range(len(r)):
        if str(r[team]['teamAbv']) == str(t):
            for player in r[team]['Roster']:
                if(r[team]['Roster'][player]['espnName']==playerName):
                    print('Found Player---------')
                    data['nbaComHeadshot']=r[team]['Roster'][player]['nbaComHeadshot']
                    data['nbaComLink']=r[team]['Roster'][player]['nbaComLink']
                    data['espnLink']=r[team]['Roster'][player]['espnLink']
                    if r[team]['Roster'][player]['injury']['injDate'] != '':
                        d = r[team]['Roster'][player]['injury']['description']
                        if len(r[team]['Roster'][player]['injury']['description']) < 5:
                            d= "No Description"
                        designation = r[team]['Roster'][player]['injury']['designation']
                        date = r[team]['Roster'][player]['injury']['injDate']
                        data['injury'] = True
                        data['designation'] = designation
                        data['date'] = date
                        data['description'] = d
                    else:
                        data['injury'] = False

    #print(teamStats)
    #save_obj(teamStats,"teamStats")
    return data

# Search result view takes player name input string
# lower case contains search all saved player names
# converts names to id's, then to season averages
# returns data for table in results view
def searchResults(request,playerName):
    context = {}
    context['playerName'] = playerName#input search context
    #load objects
    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    res = []
    #iterate over players
    for player in obj:
        #check if player name matches
        if playerName.lower() in obj[player].lower():
            p = {}
            p['name']= obj[player]
            p['id']=player
            try:
                p['seasonAverage']=seasonAverages[int(player)]
                print(seasonAverages[int(player)])
            except KeyError:
            
                print('not found')
                continue
            res.append(p)# add player to results
    context['res'] = res
    context['labels'] = labels
    # render search results page
    return render(request,'predict/searchResults.html',context)

# simple search input view
def playerSearch(request):
    context = {}
    return render(request,'predict/playerSearch.html',context)


# gets all scores dont abuse, this will take down api easily, raise time sleep 2 or 3
# dont use this on accounts with lots of junk games.
def getAllScores(request):
    qs = Game.objects.filter(author=request.user)
    for instance in qs:
        print(instance.home_score)
        if int(instance.home_score)==0:
            time.sleep(1.3)#sleep between requests
            getScore(request,instance.pk)
    return redirect('home-predict')

# renders faq page
def faq(request):
    return render(request,'predict/faq.html')




# Reset model slot, takes int model slot and gets user from requests
# Deletes the model checkpoints and saves user model settings object file.
@login_required
def resetModel(request,model):
    #if model exists delete it and its settings file
    if os.path.exists("userModels/"+str(request.user.username)+'/'+model+'/'):
        shutil.rmtree("userModels/"+str(request.user.username)+'/'+model+'/')
        os.remove("updatedObj/"+str(request.user.username) +"ModelSettings"+model+".pkl")
    return redirect('train-view',model)


# Model training view input model int
# saves checkpoints in userModels folder
# saves model settings in updatedObj folder
# Renders training view for currently selected model
@login_required
def trainView(request,model):
    context = {}
    context['model'] = model#set model int context
    username = request.user
    try:
        #load model settings
        modelSettings = load_obj(str(username.username)+'ModelSettings'+model)
        try:
            eval = modelSettings['eval']
            context['eval'] = eval
        except KeyError:
            print('no eval')
        context['showresults'] = True
        context['results'] = modelSettings['results']
        context['layer1Count']=modelSettings['layer1Count']
        context['layer1Activation']=modelSettings['layer1Activation']
        context['layer2Count']=modelSettings['layer2Count']
        context['layer2Activation']=modelSettings['layer2Activation']
        context['optimizer']=modelSettings['optimizer']
        context['epochs']=modelSettings['epochs']
        context['batchSize']=modelSettings['batchSize']
        try:
            context['es']=modelSettings['es']
            context['rmw']=modelSettings['rmw']
            context['kr']=modelSettings['kr']
            context['streaks']=modelSettings['streaks']
            context['wl']=modelSettings['wl']
            context['gp']=modelSettings['gp']
            context['ps']=modelSettings['ps']
            context['players']=modelSettings['players']

                        
            context['ast']=modelSettings['ast']
            context['blk']=modelSettings['blk']
            context['reb']=modelSettings['reb']
            context['fg3']=modelSettings['fg3']
            context['fg']=modelSettings['fg']
            context['ft']=modelSettings['ft']
            context['pf']=modelSettings['pf']
            context['pts']=modelSettings['pts']
            context['stl']=modelSettings['stl']
            context['turnover']=modelSettings['turnover']
            
        except KeyError:
            context['es']='true'
            context['rmw']='true'
            context['kr']='true'
            context['wl']='true'
            context['streaks']='true'

            context['gp']='true'
            context['ps']='true'
            context['players']=7
            context['ast']='true'
            context['blk']='true'
            context['reb']='true'
            context['fg3']='true'
            context['fg']='true'
            context['ft']='true'
            context['pf']='true'
            context['pts']='true'
            context['stl']='true'
            context['turnover']='true'

    except FileNotFoundError:
        #load defaults if no saved settings
        modelSettings = load_obj('DefaultModelSettings')
        try:
            eval = modelSettings['eval']
            context['eval'] = eval

        except KeyError:
            print('old model, no saved eval')
        context['showresults'] = True
        context['results'] = modelSettings['results']
        context['layer1Count']=modelSettings['layer1Count']
        context['layer1Activation']=modelSettings['layer1Activation']
        context['layer2Count']=modelSettings['layer2Count']
        context['layer2Activation']=modelSettings['layer2Activation']
        context['optimizer']=modelSettings['optimizer']
        context['epochs']=modelSettings['epochs']
        context['batchSize']=modelSettings['batchSize']

        try:
            context['es']=modelSettings['es']
            context['rmw']=modelSettings['rmw']
            context['kr']=modelSettings['kr']

            context['streaks']=modelSettings['streaks']
            context['wl']=modelSettings['wl']
            context['gp']=modelSettings['gp']
            context['ps']=modelSettings['ps']
            context['players']=modelSettings['players']
            
            context['ast']=modelSettings['ast']
            context['blk']=modelSettings['blk']
            context['reb']=modelSettings['reb']
            
            context['fg3']=modelSettings['fg3']
            context['fg']=modelSettings['fg']
            context['ft']=modelSettings['ft']
            context['pf']=modelSettings['pf']
            context['pts']=modelSettings['pts']
            context['stl']=modelSettings['stl']
            context['turnover']=modelSettings['turnover']
            
        except KeyError:
            context['es']='true'
            context['rmw']='true'
            context['kr']='true'
            context['streaks']='true'
            context['wl']='true'
            context['gp']='true'
            context['ps']='true'
            context['players']=7
            
            context['ast']='true'
            context['blk']='true'
            context['reb']='true'
            context['fg3']='true'
            context['fg']='true'
            context['ft']='true'
            context['pf']='true'
            context['pts']='true'
            context['stl']='true'
            context['turnover']='true'
            
    #render training page
    return render(request,'predict/train.html',context)

# makes dataset, no longer supported. might add back again oneday
@login_required
def makeDataSet(request,seasons,numgames):
    print(seasons,numgames)
    seasons = seasons.split('-')
    print(seasons)
    webData.CreateDataset(seasons,numgames)
    return redirect('train-view')


# trains a model, takes input for all the sliders and settings
# calls webappTrain from webTrain.py
@login_required
def trainModel(request,model,epochs,batchSize,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,es,rmw,kr,streaks,wl,gp,ps,players,ast,blk,reb,fg3,fg,ft,pf,pts,stl,turnover):

    username = request.user#set username of request
    context = {}
    context['model'] = model
    size = batchSize
    modelSettings = {}
    modelSettings['layer1Count']=layer1Count
    modelSettings['layer1Activation']=layer1Activation
    modelSettings['layer2Count']=layer2Count
    modelSettings['layer2Activation']=layer2Activation
    modelSettings['optimizer']=optimizer
    modelSettings['epochs']=epochs
    modelSettings['batchSize']=batchSize

    modelSettings['kr']=kr
    modelSettings['es']=es
    modelSettings['rmw']=rmw

    modelSettings['streaks']=streaks
    modelSettings['wl']=wl
    modelSettings['gp']=gp
    modelSettings['ps']=ps
    modelSettings['players']=players

    modelSettings['ast']=ast
    modelSettings['reb']=reb
    modelSettings['blk']=blk
    modelSettings['fg3']=fg3
    modelSettings['fg']=fg
    modelSettings['ft']=ft
    modelSettings['pf']=pf
    modelSettings['pts']=pts
    modelSettings['stl']=stl
    modelSettings['turnover']=turnover


    #call web train
    results = webTrain.webappTrain(model,epochs,size,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,username,es,rmw,kr,streaks,wl,gp,ps,players,ast,blk,reb,fg3,fg,ft,pf,pts,stl,turnover)
    #set results and eval
    modelSettings['results']=results[1]
    modelSettings['eval']=results[0]
    #save model settings
    save_obj(modelSettings,str(username.username)+'ModelSettings'+model)

    context['showresults'] = True
    context['results'] = results[1]
    context['layer1Count']=layer1Count
    context['layer1Activation']=layer1Activation
    context['layer2Count']=layer2Count
    context['layer2Activation']=layer2Activation
    context['optimizer']=optimizer
    context['epochs']=epochs
    context['batchSize']=batchSize
    context['es']=es
    context['rmw']=rmw
    context['kr']=kr
    context['streaks']=streaks
    context['wl']=wl
    context['gp']=gp
    context['ps']=ps
    context['players']=players
    context['ast']=ast
    context['blk']=reb
    context['fg3']=fg3
    context['fg']=fg
    context['ft']=ft
    context['pf']=pf
    context['pts']=pts
    context['stl']=stl
    context['turnover']=turnover

    context = load_obj(str(username.username)+'ModelSettings'+model)
    eval = modelSettings['eval']
    context['eval'] = eval
    context['results'] = modelSettings['results']
    context['model'] = model
    #render training page
    return render(request,'predict/train.html',context)

#Renders profile stats like margin 1-3 and win/loss with graphs.
@login_required
def statsView(request):
    context = {}
    #get a bunch of context data
    user = request.user
    context['correct'] = Profile.objects.filter(user=user).values('correct')[0]['correct']
    context['numpred'] =  Profile.objects.filter(user=user).values('predictions')[0]['predictions']
    if Profile.objects.filter(user=user).values('predictions')[0]['predictions'] >= 1:
        context['pc'] = round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)
        context['pw'] = (round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)-100)*-1
        try:
            context['extraCorrect'] = round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)-round(Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1'] /Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count'] *100)
        except ZeroDivisionError:
            context['extraCorrect'] = 0
        context['ev_won'] = Profile.objects.filter(user=user).values('ev_won')[0]['ev_won']
        context['ev_won_count'] = Profile.objects.filter(user=user).values('ev_won_count')[0]['ev_won_count']
        try:
            context['ev_won_pct'] = round(Profile.objects.filter(user=user).values('ev_won')[0]['ev_won'] /Profile.objects.filter(user=user).values('ev_won_count')[0]['ev_won_count'] *100)
        except ZeroDivisionError:
            context['ev_won_pct'] = 0
        context['ev_margin1'] = Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1']
        context['ev_margin1_count'] = Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count']
        try:
            context['ev_margin1_pct'] = round(Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1'] /Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count'] *100)
        except ZeroDivisionError:
            context['ev_margin1_pct'] = 0

        context['ev_margin2'] = Profile.objects.filter(user=user).values('ev_margin2')[0]['ev_margin2']
        context['ev_margin2_count'] = Profile.objects.filter(user=user).values('ev_margin2_count')[0]['ev_margin2_count']
        try:
            context['ev_margin2_pct'] = round(Profile.objects.filter(user=user).values('ev_margin2')[0]['ev_margin2'] /Profile.objects.filter(user=user).values('ev_margin2_count')[0]['ev_margin2_count'] *100)
        except ZeroDivisionError:
            context['ev_margin2_pct'] = 0
        context['ev_margin3'] = Profile.objects.filter(user=user).values('ev_margin3')[0]['ev_margin3']
        context['ev_margin3_count'] = Profile.objects.filter(user=user).values('ev_margin3_count')[0]['ev_margin3_count']
        try:
            context['ev_margin3_pct'] = round(Profile.objects.filter(user=user).values('ev_margin3')[0]['ev_margin3'] /Profile.objects.filter(user=user).values('ev_margin3_count')[0]['ev_margin3_count'] *100)
        except ZeroDivisionError:
            context['ev_margin3_pct'] = 0

    else:
        context['ev_margin1'] = 0
        context['ev_margin1_count'] = 0
        context['ev_margin1_pct'] = 0
        context['ev_margin2'] = 0
        context['ev_margin2_count'] =0
        context['ev_margin2_pct'] = 0
        context['ev_margin3'] = 0
        context['ev_margin3_count'] = 0
        context['ev_margin3_pct'] = 0


        context['pc'] = '0'
    context['gain'] =  Profile.objects.filter(user=user).values('gain')[0]['gain']
    context['loss'] =  Profile.objects.filter(user=user).values('loss')[0]['loss']
    context['lg'] = Profile.objects.filter(user=user).values('gain')[0]['gain'] - Profile.objects.filter(user=user).values('loss')[0]['loss']
    
    qs = Message.objects.order_by('id')[:100]
    profiles = Profile.objects.order_by('id')
    context['profiles'] = profiles
    context['qs']=qs
    #render page
    #this page is also rendering chat and users list
    #probably can be removed from github version, only really needed live
    #for now i will leave it
    return render(request,'predict/stats.html',context)

# Remove player from game
# takes game pk id and player id
# adds player id to blacklisted players and recreates game without player..
# redirects back to game edit view
def removePlayer(request,pk,player):
    print(pk)#game pk
    print(player)#player name
    obj = load_obj('2019PlayerNamesByID')
    player_id =''
    for id in obj:
        if obj[id].replace("'", "-") == player:#convert ' apostrophe with - dash
            print(id)
            player_id = id#found player id
            break
    #get game object instance
    g = Game.objects.filter(pk=pk)
    #set values
    home = g.values('home')[0]['home']
    visitor = g.values('visitor')[0]['visitor']
    csvid = g.values('csvid')[0]['csvid']
    date = g.values('gamedate')[0]['gamedate']
    #get old removed players
    removed_players=g.values('removed_players')[0]['removed_players']
    date=g.values('gamedate')[0]['gamedate']
    #if already removed a player
    if removed_players is not None:
        removed_players = json.loads(removed_players)
        # add new removed played to already removed players
        removed_players.append(str(player_id))
    else:
        #else first removed player
        removed_players = []
        removed_players.append(str(player_id))
    removed_players_dump = json.dumps(removed_players)
    season = '2022'
    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
    #path to csv file for prediction
    path = 'csv/'+str(request.user)+str(csvid)+'.csv'
    #get current spread
    spread = getSpread(home,visitor,date)
    #set spread values
    home_spread = spread[0]
    visitor_spread = spread[1]
    #get team data
    stats = getTeamData(home,visitor)
    #set team data
    homeTeamStats = stats[0]
    homeTeamInjuryComplex = homeTeamStats.pop(-1)

    homeTeamInjury = homeTeamStats.pop(-1)
    
    visitorTeamStats = stats[1]
    visitorTeamInjuryComplex = visitorTeamStats.pop(-1)
    visitorTeamInjury = visitorTeamStats.pop(-1)
    
    home_streak = homeTeamStats.pop(-1)
    visitor_streak = visitorTeamStats.pop(-1)

    #print('spread: ', spread)
    homeTeamInjuryComplex = json.dumps(homeTeamInjuryComplex)
    visitorTeamInjuryComplex = json.dumps(visitorTeamInjuryComplex)
    #get future game
    found, gameid, playerids,asd,dsa,das,foobar = futureGame(home_spread,homeTeamStats,visitorTeamStats,date,home,visitor,path,season,labels,removed_players)

    #set simple injury data
    homeInjury = ''
    for player in homeTeamInjury:
        homeInjury += ', '+player
    if homeInjury != '':
        homeInjury = homeInjury[1:]
    visitorInjury = ''
    for player in visitorTeamInjury:
        visitorInjury += ', '+player
    if visitorInjury != '':
        visitorInjury = visitorInjury[1:]
    #update game with values
    g.update(author=request.user,home=home,visitor=visitor,gamedate=date,homecolor=TEAMCOLORS[home],visitorcolor=TEAMCOLORS[visitor],csvid=csvid,
        p0 = playerids[0], p1 = playerids[1], p2 = playerids[2], p3 = playerids[3], p4 = playerids[4], p5 = playerids[5],
        p6 = playerids[6], p7 = playerids[7], p8 = playerids[8], p9 = playerids[9], p10 = playerids[10], p11 = playerids[11],
        p12 = playerids[12], p13 = playerids[13],
        gameid=gameid,home_spread=home_spread,visitor_spread=visitor_spread,dk_home_spread=home_spread,dk_visitor_spread=visitor_spread,
        home_games_won=homeTeamStats[1],home_games_loss=homeTeamStats[2],
        visitor_games_won=visitorTeamStats[1],visitor_games_loss=visitorTeamStats[2],home_streak=home_streak,visitor_streak=visitor_streak,
        homeInjury=homeInjury, visitorInjury=visitorInjury,removed_players=removed_players_dump,homeInjuryComplex=homeTeamInjuryComplex,visitorInjuryComplex=visitorTeamInjuryComplex)
    #redirect back to game
    return redirect('edit-predict',pk)





# creates csv file with all games on account. 
# exports them and supplies an instant download.
def exportGames(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    # http header
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    # csv header
    header = ['gameid','gamedate','home','visitor','margin','spread_prediction','won_vs_spread','home_score','visitor_score','home_score_prediction','visitor_score_prediction','home_spread','visitor_spread','home_games_won','home_games_loss','visitor_games_won','visitor_games_loss','pmscore','home_injury','visitor_injury','removed_players']    
    #create writer
    writer = csv.writer(response)
    #write header
    writer.writerow(header)
    #get request user
    user = request.user
    #get that users games
    qs = Game.objects.filter(author=user)
    lines = []
    #loop over games
    for game in qs:
        g = [game.gameid,game.gamedate,game.home,game.visitor,game.margin,game.spread_prediction,game.ev_won,game.home_score,game.visitor_score,
        game.home_score_prediction,game.visitor_score_prediction,game.home_spread,game.visitor_spread,
        game.home_games_won,game.home_games_loss,game.visitor_games_won,game.visitor_games_loss,game.pmscore,game.homeInjury,game.visitorInjury,game.removed_players]
        line = []
        for s in g:
            line.append(str(s))
        #create lines object
        lines.append(line)
    #write lines
    for line in lines:
        writer.writerow(line)
    #return the file
    return response


# Saved edited game stats, and makes prediction
# takes model slot to user, pk id of game, and str of any changes made to stats
# returns redirect to dashboard, maybe change this to redirect back to edit view not sure.
def saveEdit(request,model,pk,change,**kwargs):

    model = str(model)#set model int number
    username = request.user#set user name
    #convert changes input str to changes list
    changes = change[7:].split('-')
    changes.pop(-1)
    print(changes)
    context = {}
    user = request.user
    #get game object
    g = Game.objects.filter(pk=pk)
    #get csvid
    csvid = g.values('csvid')[0]['csvid']
    #set path
    path = 'csv/'+str(user.username)+str(csvid)+'.csv'
    csv = open(path,'r')
    first=True
    data = ''
    header = ''

    for line in csv.readlines():
        print(line)
        if first:
            header = line
            first = False
        else:
            data = line#get old data before changes
            break
    #split old data and head into lists
    data = data.split(',')
    header= header.split(',')
    print(path,data,'-------')
    #pop game id, home and visitor team stats and spread
    #doing this to leave only player data
    #the player data is then mapped against any changes to the input data
    gameid = data.pop(0)
    header.pop(0)
    
    data.pop(0)
    header.pop(0)

    homeid = data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)

    visitorid = data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)

    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
    print(header)
    print(data)
    #loop through changes
    for c in changes:
        x = c.split(':')#specific change being made
        n=17*int(x[0])-17+int(x[1])#where in data needs to be changed
        data[n-2]=x[2]#update new data
        print(n)
        print(data[n-2])
    print(data,'fffffffffffff')

    #write csv header
    writeCSVHeader(labels, path)
    #write csv file with changes to data applied
    def w(data, path, g):
        hgp = int(g.values('home_games_won')[0]['home_games_won'])+int(g.values('home_games_loss')[0]['home_games_loss'])
        spread = str(g.values('home_spread')[0]['home_spread'])
        vgp = int(g.values('visitor_games_won')[0]['visitor_games_won'])+int(g.values('visitor_games_loss')[0]['visitor_games_loss'])
        home_streak = int(g.values('home_streak')[0]['home_streak'])
        visitor_streak = int(g.values('visitor_streak')[0]['visitor_streak'])
        ss = str(g.values('gameid')[0]['gameid'])+','+spread+','+homeid+','+str(home_streak)+','+str(hgp)
        ss+=','+str(int(g.values('home_games_won')[0]['home_games_won']))+','+str(int(g.values('home_games_loss')[0]['home_games_loss']))
        ss+=','+visitorid+','+str(visitor_streak)+','+str(vgp)
        ss+=','+str(int(g.values('visitor_games_won')[0]['visitor_games_won']))+','+str(int(g.values('visitor_games_loss')[0]['visitor_games_loss']))
        for st in data:
            ss+=','+st
        print('$$$$$$$$$',ss)
        print(path)
        f = open(path,'a')#open path
        f.write(ss+'\n')#write file
    w(data, path,g)  
    p = predict(model,path,username)#predict game
    print(p)

    #Set a bunch of values based on the prediction

    pmscore = float(p[0]-p[1])#plus minus prediction score 
    spread = float(g.values('home_spread')[0]['home_spread'])*-1#spread used to make prediction
    margin = abs(spread-pmscore)# calculate margin
    print('spread ',g.values('home_spread')[0]['home_spread'],'pmscore ',p[0]-p[1])
    print('spread ',spread,'pmscore ',pmscore)
    if float(pmscore) < 0 and float(spread) < 0:
        print('both negative')#think this not need anymore
        #there was an issue here but i think abs(spread-pmscore) fixed it
        #margin = pmscore+spread
    #set game obj values
    g.update(home_score_prediction=round(p[0],2))
    g.update(visitor_score_prediction=round(p[1],2))
    g.update(pmscore=p[0]-p[1])
    g.update(margin=abs(margin))
    g.update(model=model)
    spread = float(g.values('home_spread')[0]['home_spread'])*-1#did this twice
    #calculate spread prediction 0 if predicting visitor 1 for home
    pmp = pmscore
    print(spread,pmp)
    pred = None
    if spread>pmp and pmp <0:
        pred = 0
    elif spread>pmp and pmp >0:
        pred = 0
    elif spread<pmp and pmp <0:
        pred = 1
    elif spread<pmp and pmp >0:
        pred = 1
    #set that value
    g.update(spread_prediction=pred)
    #redirect back to dashboard maybe change in future to redirect back to game.
    return redirect('home-predict')



# Main game view, Shows teams prediction model selector, tables, injuries, and more...
# takes game pk id as input and return render of predict/edit.html
def editGame(request,pk,**kwargs):
    context = {}
    #get user and game
    user = request.user
    g = Game.objects.filter(pk=pk)
    csvid = g.values('csvid')[0]['csvid']
    gID = g.values('gameid')[0]['gameid']
    author = g.values('author')[0]['author']
    u = User.objects.filter(id=author).first()
    print('gID:', gID)
    #game is messed up redirect home
    if gID is None:
        return redirect('home-predict')
    #get labels
    def get_labels():
        lol= []
        ll = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for l in ll:
            lol.append(l.upper())
        return lol

    context['labels']= get_labels()

    path = 'csv/'+str(u.username)+str(csvid)+'.csv'
    csv = open(path,'r+')
    header = ''
    data= ''
    first = True
    for line in csv.readlines():
        if first:
            header = line
            first = False
        else:
            data = line
            break
    data = data.split(',')
    header= header.split(',')
    #pop game id, home and visitor team stats and spread
    #doing this to leave only player data
    #the player data is then mapped against any changes to the input data
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)
    #game already predicted? remove those values too
    if g.values('visitor_score_prediction')[0]['visitor_score_prediction'] is not None:
        data.pop(0)
        header.pop(0)
        data.pop(0)
        header.pop(0)
    players = {}
    oofnog = []#oofnog
    for i in range(0,14):
        #print(g.values('p'+str(i))[0]['p'+str(i)])
        #adding player ids
        oofnog.append(g.values('p'+str(i))[0]['p'+str(i)])
    url = 'https://www.balldontlie.io/api/v1/players/'
    resp = []
    #print(oofnog)
    for id in oofnog:#getting player names
        obj = load_obj('2019PlayerNamesByID')
        #print(resp)
        found = False
        for x in obj:

            if int(x) == int(id):
                found = True
                print('found-------')
                resp.append(obj[x].replace("'", "-"))

        if not found:#cant find name request it from api
            r = req(url+str(id))
            fn = r['first_name']
            ln = r['last_name']
            full = fn+' '+ln
            resp.append(full)
            obj.update({str(id) : full})
            save_obj(obj,'2019PlayerNamesByID')
    #set players
    c = 0
    for oof in range(1,15):
        n=17*oof-17
        temp = [str(oof)]
        for f in range(n,n+17):
            temp.append(data[f])

        players.update({ resp[c] : temp })
        c+=1
    #set context data
    context['pk'] = pk
    context['stats']= players
    context['home']=g.values('home')[0]['home']
    context['homecolor']=g.values('homecolor')[0]['homecolor']
    context['visitorcolor']=g.values('visitorcolor')[0]['visitorcolor']
    context['visitor']=g.values('visitor')[0]['visitor']
    context['gamedate']=g.values('gamedate')[0]['gamedate']
    context['home_score']=g.values('home_score')[0]['home_score']
    context['visitor_score']=g.values('visitor_score')[0]['visitor_score']
    context['home_spread']=g.values('home_spread')[0]['home_spread']
    context['visitor_spread']=g.values('visitor_spread')[0]['visitor_spread']
    context['dk_home_spread']=g.values('dk_home_spread')[0]['dk_home_spread']
    context['dk_visitor_spread']=g.values('dk_visitor_spread')[0]['dk_visitor_spread']
    context['prediction']=g.values('prediction')[0]['prediction']
    context['finished']=g.values('finished')[0]['finished']
    context['winner'] = g.values('winner')[0]['winner']
    context['pmscore'] = g.values('pmscore')[0]['pmscore']

    context['pmactual'] = int(g.values('home_score')[0]['home_score'])-int(g.values('visitor_score')[0]['visitor_score'])

    context['pvscore'] = g.values('visitor_score_prediction')[0]['visitor_score_prediction']
    context['phscore'] = g.values('home_score_prediction')[0]['home_score_prediction']

    context['hw'] = g.values('home_games_won')[0]['home_games_won']
    context['hl'] = g.values('home_games_loss')[0]['home_games_loss']

    context['vw'] = g.values('visitor_games_won')[0]['visitor_games_won']
    context['vl'] = g.values('visitor_games_loss')[0]['visitor_games_loss']

    context['home_streak'] = g.values('home_streak')[0]['home_streak']
    context['visitor_streak'] = g.values('visitor_streak')[0]['visitor_streak']
    context['margin'] = g.values('margin')[0]['margin']
    context['csvid'] = g.values('csvid')[0]['csvid']
    context['date_posted'] = g.values('date_posted')[0]['date_posted']
    context['gameid'] = g.values('gameid')[0]['gameid']
    context['finished'] = g.values('finished')[0]['finished']
    context['removed_players'] = g.values('removed_players')[0]['removed_players']
    context['ev_won'] = g.values('ev_won')[0]['ev_won']
    context['author'] = u
    context['spread_prediction'] = g.values('spread_prediction')[0]['spread_prediction']

    if g.values('homeInjuryComplex')[0]['homeInjuryComplex'] is not None:
        context['hInjuryComplex'] = json.loads(g.values('homeInjuryComplex')[0]['homeInjuryComplex'])
        context['hInjuryDisplay'] = True
    else:
        context['hInjuryDisplay'] = False
        context['hInjuryComplex'] = []
    if g.values('visitorInjuryComplex')[0]['visitorInjuryComplex'] is not None:
        context['vInjuryComplex'] = json.loads(g.values('visitorInjuryComplex')[0]['visitorInjuryComplex'])
        context['vInjuryDisplay'] = True

    else:
        context['vInjuryComplex'] = []
        context['vInjuryDisplay'] = False
    hi = g.values('homeInjury')[0]['homeInjury']
    if hi is None:
        context['home_injury'] = 0
        context['home_injuries'] = 0
    else:
        hi = hi.split(',')
        context['home_injury'] = len(hi)
        context['home_injuries'] = g.values('homeInjury')[0]['homeInjury']


    vi = g.values('visitorInjury')[0]['visitorInjury']
    if vi is None:
        context['visitor_injury'] = 0
        context['visitor_injuries'] = 0
       
    else:
        vi = vi.split(',')
        context['visitor_injury'] = len(vi)
        context['visitor_injuries'] = g.values('visitorInjury')[0]['visitorInjury']
        
    context['game'] = g
    context['g'] = g
    context['model']=g.values('model')[0]['model']
    context['bet']=g.values('bet')[0]['bet']
    try:
        modelSettings = load_obj(str(request.user.username)+'ModelSettings'+g.values('model')[0]['model'])
        context['customModel']=True
        
    except FileNotFoundError:
        context['customModel']=False
    
    

    #set complex spread
    if g.values('complexSpread')[0]['complexSpread'] is not None:
        foo = json.loads(g.values('complexSpread')[0]['complexSpread'])
        complexSpread = []
        for k in foo:
            foo[k]['name'] = k
            complexSpread.append(foo[k])
        context['complexSpread'] = sortSpreadLines(complexSpread) 
        
        context['complexSpreadDisplay'] = True
    context['history_display'] = True
    #set is your game
    if request.user == u:
        context['isAuthor'] = True
    else:
        context['isAuthor'] = False
        
    teamAbvById = load_obj('teamAbvById')
    context['home_history_id'] = g.values('home_last_game')[0]['home_last_game']
    context['visitor_history_id'] = g.values('visitor_last_game')[0]['visitor_last_game']
    try:
        hh = json.loads(g.values('home_history')[0]['home_history'])

    except TypeError:
        context['history_display'] = False

        return render(request, 'predict/edit.html',context)
    

    obj = load_obj('2019PlayerNamesByID')
    for player in hh[0]:
        print('player: ',player)
        id = player['id']
        player.pop('teamid')
        try:
            try:
                player['name']=obj[str(id)]
            except KeyError:
                player['name']=obj[int(id)]
        except KeyError:
            player['name']=id
    for player in hh[1]:
        print('player: ',player)
        id = player['id']
        player.pop('teamid')
        try:
            try:
                player['name']=obj[str(id)]
            except KeyError:
                player['name']=obj[int(id)]
        except KeyError:
            player['name']=id


    context['hh_players'] = hh[0]
    context['hh_op_player'] = hh[1]
    context['hh_score'] = hh[2]
    context['hh_op_score'] = hh[3]
    context['hh_gameid'] = hh[4]
    context['hh_op_abv'] = teamAbvById[int(hh[5])]
    context['hh_date'] = hh[6][:10]

    vh = json.loads(g.values('visitor_history')[0]['visitor_history'])
    context['vh_players'] = vh[0]
    for player in vh[0]:
        print('player: ',player)
        id = player['id']
        player.pop('teamid')
        try:
            try:
                player['name']=obj[str(id)]
            except KeyError:
                player['name']=obj[int(id)]
        except KeyError:
            player['name']=id
    for player in vh[1]:
        print('player: ',player)
        id = player['id']
        player.pop('teamid')
        try:
            try:
                player['name']=obj[str(id)]
            except KeyError:
                player['name']=obj[int(id)]
        except KeyError:
            player['name']=id

    context['vh_op_player'] = vh[1]
    context['vh_score'] = vh[2]
    context['vh_op_score'] = vh[3]
    context['vh_gameid'] = vh[4]
    context['vh_op_abv'] = teamAbvById[int(vh[5])]
    context['vh_date'] = vh[6][:10]

    print(hh)
    #context['home_history'] = 



    #print(players)
    #render main game page.
    return render(request, 'predict/edit.html',context)




# Sort spread lines min to max, takes complex spread obj and returns sorted list
def sortSpreadLines(complexSpread):
    sorted = []
    while len(complexSpread)>0:
        min = 100000
        index = None
        for line in range(len(complexSpread)):
            print(line)
            if complexSpread[line]['awayTeamSpread'] == 'PK':
                complexSpread[line]['awayTeamSpread'] = 0
            if complexSpread[line]['homeTeamSpread'] == 'PK':
                complexSpread[line]['homeTeamSpread'] = 0
            if float(complexSpread[line]['homeTeamSpread']) < min:
                min = float(complexSpread[line]['homeTeamSpread'])
                index = line
        sorted.append(complexSpread[index])
        complexSpread.pop(index)

    return sorted

# get score for a game
# take game pk id and request api
# if game is final the scores are used to calculate prediction correct or wrong
# profile stats are then updated to match
# returns redirect to dashboard
def getScore(request,pk,**kwargs):

    url = 'https://www.balldontlie.io/api/v1/games/'
    user= request.user
    g = Game.objects.filter(pk=pk).values('gameid')
    g = g[0]
    url += g['gameid']
    r = req(url)#request api for scores
    h = r['home_team_score']#set home score
    v= r['visitor_team_score']# set visitor score
    print(request.user,'-----------------')
    p = Profile.objects.filter(user=request.user)
    po = Profile.objects.get(user=request.user)

    if r['status'] == "Final":#is game score final??
        #set final values and calculate correct not and at what margin level?
        prediction = Game.objects.filter(pk=pk).values('prediction')[0]['prediction']
        pmscore = Game.objects.filter(pk=pk).values('pmscore')[0]['pmscore']
        finished = Game.objects.filter(pk=pk).values('finished')[0]['finished']
        spread = Game.objects.filter(pk=pk).values('home_spread')[0]['home_spread']
        home_score = Game.objects.filter(pk=pk).values('home_score')[0]['home_score']
        visitor_score = Game.objects.filter(pk=pk).values('visitor_score')[0]['visitor_score']

        if not finished: # add not back
            spread = float(spread)*-1
            if pmscore >= 0 and h >v:#win p home
                asdf = float(p.values('gain')[0]['gain'])
                p.update(gain=asdf+abs(pmscore))
                p.update(correct=p.values('correct')[0]['correct']+1)
                Game.objects.filter(pk=pk).update(winner=1)
            if pmscore < 0 and h < v:#win p visitor
                asdf = float(p.values('gain')[0]['gain']) 
                p.update(gain=asdf+abs(pmscore))
                p.update(correct=p.values('correct')[0]['correct']+1)
                Game.objects.filter(pk=pk).update(winner=0)
            if pmscore < 0 and h > v:#loose p vis
                asdf = float(p.values('loss')[0]['loss']) 
                p.update(loss=asdf+abs(pmscore))
                Game.objects.filter(pk=pk).update(winner=1)
            if pmscore >= 0 and h < v:#loose p home
                print('asdf')
                asdf = float(p.values('loss')[0]['loss']) 
                p.update(loss=asdf+abs(pmscore))
                Game.objects.filter(pk=pk).update(winner=0)
            print(Game.objects.filter(pk=pk).values('winner')[0]['winner'])
            p.update(predictions=p.values('predictions')[0]['predictions']+1)


            pmp = pmscore
            pmscore = int(h)-int(v)
            margin = float(Game.objects.filter(pk=pk).values('margin')[0]['margin'])
            pred = ''
            print(spread,pmp)

            if spread>pmp and pmp <0:
                pred = 0
            elif spread>pmp and pmp >0:
                pred = 0
            elif spread<pmp and pmp <0:
                pred = 1
            elif spread<pmp and pmp >0:
                pred = 1

            swin = ''#winner with spread 0 or 1 
            print(spread,pmscore)
            print(float(spread)<float(pmscore))
            print(float(pmscore)>0)
            if spread>pmscore and pmscore <0:
                swin = 0
            elif spread>pmscore and pmscore >0:
                swin = 0
            elif spread<pmscore and pmscore <0:
                swin = 1
            elif spread<pmscore and pmscore >0:
                swin = 1
            print('swin',swin)
            print('pred:',pred)
            print('pred , swin :',pred,swin)
            mcorrect = False
            #set ev_won same as margin 0....
            if pred == 0 and swin == 0:
                mcorrect = True
                Game.objects.filter(pk=pk).update(ev_won='1')

                print('correct agaist spread',pred,swin)
            elif pred == 1 and swin == 1:
                Game.objects.filter(pk=pk).update(ev_won='1')
                mcorrect = True
                print('correct agaist spread',pred,swin)
            else:
                Game.objects.filter(pk=pk).update(ev_won='0')
                mcorrect = False
                print('wrong agaist spread pred:',pred,' swin',swin)

            #set margin 1-3 
            if abs(margin) > 3:
                if mcorrect:
                    Game.objects.filter(pk=pk).update(ev_margin3='1')
                    asdf = int(p.values('ev_margin3')[0]['ev_margin3']) 
                    p.update(ev_margin3=asdf+1)
                asdf = int(p.values('ev_margin3_count')[0]['ev_margin3_count']) 
                p.update(ev_margin3_count=asdf+1)
            if abs(margin) > 2:
                if mcorrect:
                    Game.objects.filter(pk=pk).update(ev_margin2='1')
                    asdf = int(p.values('ev_margin2')[0]['ev_margin2']) 
                    p.update(ev_margin2=asdf+1)
                asdf = int(p.values('ev_margin2_count')[0]['ev_margin2_count']) 
                p.update(ev_margin2_count=asdf+1)
            if abs(margin) > 1:
                if mcorrect:
                    Game.objects.filter(pk=pk).update(ev_margin1='1')
                    asdf = int(p.values('ev_margin1')[0]['ev_margin1']) 
                    p.update(ev_margin1=asdf+1)
                asdf = int(p.values('ev_margin1_count')[0]['ev_margin1_count']) 
                p.update(ev_margin1_count=asdf+1)

            if mcorrect:
                asdf = int(p.values('ev_won')[0]['ev_won']) 
                p.update(ev_won=asdf+1)
            asdf = int(p.values('ev_won_count')[0]['ev_won_count']) 
            p.update(ev_won_count=asdf+1)


        #set game finished
        Game.objects.filter(pk=pk).update(finished=True)
    #set scores
    Game.objects.filter(pk=pk).update(home_score=h)
    Game.objects.filter(pk=pk).update(visitor_score=v)
    #print(pagenum)
    #x = redirect("home-predict")
    #return HttpResponsePermanentRedirect(reverse('home-predict') + "?page="+str(page_num))
    #redirect back home, there is a bug where it always redirects to page 1 even if your on page 5....
    try:
        r = kwargs['redirect']
        return redirect('edit-predict',pk)

    except KeyError:
        return redirect('home-predict')



# takes date str, request's api, and returns list of games


from dateutil.parser import parse
from zoneinfo import ZoneInfo
#replace with this import if on older python version
#from backports.zoneinfo import ZoneInfo

# takes date str, request's api, and returns list of games
def todaysGames(date):
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    eastern = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d'
    loc_dt = datetime.now(eastern)
    #naive_dt = datetime.now()
    url+=date#create api url with current date
    print(url)
    r = req(url)#request api url
    games = []
    for game in range(len(r['data'])):#iterate over response and create games obj
        habv = r['data'][game]['home_team']['abbreviation']
        hfn = r['data'][game]['home_team']['full_name']
        hscore = str(r['data'][game]['home_team_score'])
        vabv = r['data'][game]['visitor_team']['abbreviation']
        vfn = r['data'][game]['visitor_team']['full_name']
        vscore = str(r['data'][game]['visitor_team_score'])
        status = r['data'][game]['status']
        print(status)
        old=False
        if status != 'Final':
            try:
                status = datetime.strptime(str(status), '%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo("US/Eastern")).strftime('%I:%M %p')
            except ValueError:
                print('something went wrong')
        foo = {'habv':habv,'hfn':hfn,'hscore':hscore,'vabv':vabv,'vfn':vfn,'vscore':vscore,'status':status,'date':date}
        games.append(foo)
    if len(games)==0:#set no games today
        games.append('No Games Today')
    return games


#Main dashboard game list view.
class GameListView(ListView, LoginRequiredMixin):
    model = Game
    template_name = 'predict/home.html'
    ordering = ['-date_posted']#sort games by date posted
    paginate_by = 20#number to of games on each page
    context_object_name = 'games'
    context = 'games'

    def get_context_data(self, **kwargs):
        #get context data
        try:
            dateSelected = self.kwargs['dateSelected']
        except KeyError:
            eastern = timezone('America/Los_Angeles')
            fmt = '%Y-%m-%d'
            loc_dt = datetime.now(eastern)
            #naive_dt = datetime.now()
            dateSelected =loc_dt.strftime(fmt)
             
        print(dateSelected)
        user = self.request.user
        context = super(GameListView, self).get_context_data(**kwargs)
        x = todaysGames(dateSelected)
        context['today'] = x
        context['tc'] = TEAMCOLORS
        context['correct'] = Profile.objects.filter(user=user).values('correct')[0]['correct']
        context['numpred'] =  Profile.objects.filter(user=user).values('predictions')[0]['predictions']
        if Profile.objects.filter(user=user).values('predictions')[0]['predictions'] >= 1:
            context['pc'] = round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)
            context['pw'] = (round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)-100)*-1
            try:
                context['extraCorrect'] = round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)-round(Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1'] /Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count'] *100)
            except ZeroDivisionError:
                context['extraCorrect'] = 0
            context['ev_margin1'] = Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1']
            context['ev_margin1_count'] = Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count']
            try:
                context['ev_margin1_pct'] = round(Profile.objects.filter(user=user).values('ev_margin1')[0]['ev_margin1'] /Profile.objects.filter(user=user).values('ev_margin1_count')[0]['ev_margin1_count'] *100)
            except ZeroDivisionError:
                context['ev_margin1_pct'] = 0

            context['ev_margin2'] = Profile.objects.filter(user=user).values('ev_margin2')[0]['ev_margin2']
            context['ev_margin2_count'] = Profile.objects.filter(user=user).values('ev_margin2_count')[0]['ev_margin2_count']
            try:
                context['ev_margin2_pct'] = round(Profile.objects.filter(user=user).values('ev_margin2')[0]['ev_margin2'] /Profile.objects.filter(user=user).values('ev_margin2_count')[0]['ev_margin2_count'] *100)
            except ZeroDivisionError:
                context['ev_margin2_pct'] = 0
            context['ev_margin3'] = Profile.objects.filter(user=user).values('ev_margin3')[0]['ev_margin3']
            context['ev_margin3_count'] = Profile.objects.filter(user=user).values('ev_margin3_count')[0]['ev_margin3_count']
            try:
                context['ev_margin3_pct'] = round(Profile.objects.filter(user=user).values('ev_margin3')[0]['ev_margin3'] /Profile.objects.filter(user=user).values('ev_margin3_count')[0]['ev_margin3_count'] *100)
            except ZeroDivisionError:
                context['ev_margin3_pct'] = 0

        else:
            context['ev_margin1'] = 0
            context['ev_margin1_count'] = 0
            context['ev_margin1_pct'] = 0
            context['ev_margin2'] = 0
            context['ev_margin2_count'] =0
            context['ev_margin2_pct'] = 0
            context['ev_margin3'] = 0
            context['ev_margin3_count'] = 0
            context['ev_margin3_pct'] = 0


            context['pc'] = '0'
        context['gain'] =  Profile.objects.filter(user=user).values('gain')[0]['gain']
        context['loss'] =  Profile.objects.filter(user=user).values('loss')[0]['loss']
        context['lg'] = Profile.objects.filter(user=user).values('gain')[0]['gain'] - Profile.objects.filter(user=user).values('loss')[0]['loss']
        
        #context['form'] = GameForm()
        context['dateselector'] = dateSelected

        context['ordering']= ['-date_posted']
        return context
    #get list of games 
    def get_queryset(self, **kwargs):
        user = self.request.user
        return Game.objects.filter(author=user).order_by('-date_posted')
    #old not used anymore
    def form_valid(self, form):
        print('-------------------')
        form.instance.author = self.request.user
        season = '2022'

        path = 'csv/'+str(form.instance.pk)+'.csv'
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        x = form.instance.gamedate
        y = form.instance.home.upper()
        z = form.instance.visitor.upper()
        date=x
        homeAbv=y
        visitorAbv=z
        found, gameid = futureGame(date, homeAbv,visitorAbv,path,season,labels)
        if found:
            form.instance.gameid = gameid
        else:
            form.instance.gameid = 'error'
        return super().form_valid(form)



# Predict all button below todays games
# takes date and model select, loops over games and predicts them
# thing to note is no players are removed automatically
# returns redirect for dashboard
def predictAll(request,dateSelected,model,**kwargs):
    print(dateSelected)
    #get todays games
    tg = todaysGames(dateSelected)
    print(tg)
    model = str(model)
    for game in tg:#for game in todays games
        #create game using quick create function
        quickcreate(request,game['habv'],game['vabv'],game['date'])
        #Get the game we just created
        g = Game.objects.filter(author=request.user).order_by('-date_posted').first()
        #predict the game using model input int
        saveEdit(request,model,g.pk,'',**kwargs)
    #redirect back home
    return redirect('home-predict')

# creates game clicked on from callender
# takes home visitor team abv, and selected date
# request api loads teams and player stats
# returns redirect to game edit view
def quickcreate(request,home,visitor,date):

    #make up a random csvid 
    csvid = random.randint(1,100000)
    #set season #this will probably need manual updating in future
    season = '2022'
    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
    #set path to csv
    path = 'csv/'+str(request.user)+str(csvid)+'.csv'

    #get spread
    spread = getSpread(home,visitor,date)
    print(spread)
    home_spread = spread[0]
    visitor_spread = spread[1]
    try:
        complexSpread = spread[2]
        complexSpread=json.dumps(complexSpread)
    except IndexError:
        complexSpread = []
    #get team and injury data
    stats = getTeamData(home,visitor)
    homeTeamStats = stats[0]
    homeTeamInjuryComplex = homeTeamStats.pop(-1)
    homeTeamInjury = homeTeamStats.pop(-1)
    visitorTeamStats = stats[1]
    visitorTeamInjuryComplex = visitorTeamStats.pop(-1)
    visitorTeamInjury = visitorTeamStats.pop(-1)
    
    home_streak = homeTeamStats.pop(-1)
    visitor_streak = visitorTeamStats.pop(-1)
    homeTeamInjuryComplex = json.dumps(homeTeamInjuryComplex)
    visitorTeamInjuryComplex = json.dumps(visitorTeamInjuryComplex)
    removed_players = []
    #create future game
    found, gameid, playerids, hLastGame,vLastGame,home_history,visitor_history = futureGame(home_spread,homeTeamStats,visitorTeamStats,date,home,visitor,path,season,labels,removed_players)
    #set simple injury data
    homeInjury = ''
    for player in homeTeamInjury:
        homeInjury += ', '+player
    if homeInjury != '':
        homeInjury = homeInjury[1:]
    visitorInjury = ''
    for player in visitorTeamInjury:
        visitorInjury += ', '+player
    if visitorInjury != '':
        visitorInjury = visitorInjury[1:]

    #create game object instance
    obj = Game.objects.create(author=request.user,home=home,visitor=visitor,gamedate=date,homecolor=TEAMCOLORS[home],visitorcolor=TEAMCOLORS[visitor],csvid=csvid,
        p0 = playerids[0], p1 = playerids[1], p2 = playerids[2], p3 = playerids[3], p4 = playerids[4], p5 = playerids[5],
        p6 = playerids[6], p7 = playerids[7], p8 = playerids[8], p9 = playerids[9], p10 = playerids[10], p11 = playerids[11],
        p12 = playerids[12], p13 = playerids[13],
        gameid=gameid,home_spread=home_spread,visitor_spread=visitor_spread,dk_home_spread=home_spread,dk_visitor_spread=visitor_spread,
        home_games_won=homeTeamStats[1],home_games_loss=homeTeamStats[2],
        visitor_games_won=visitorTeamStats[1],visitor_games_loss=visitorTeamStats[2],home_streak=home_streak,visitor_streak=visitor_streak,
        homeInjury=homeInjury, visitorInjury=visitorInjury,homeInjuryComplex=homeTeamInjuryComplex,visitorInjuryComplex=visitorTeamInjuryComplex,complexSpread=complexSpread,home_last_game=hLastGame,visitor_last_game=vLastGame,
        home_history=home_history,visitor_history=visitor_history)
    #redirect to game view
    return redirect('edit-predict',obj.pk)
    #return redirect('home-predict')


# Gets team data win/loss/streak
# takes home and visitor abv
# returns [teamStats[h],teamStats[v]]
def getTeamData(home,visitor):
    #convert abv from api 1 to api 2
    #1 being balldontlie.io
    #2 being tank01 rapid api nba fantasy sports
    convert = {
        'ATL' :'ATL',
        'BKN':  'BKN',
        'BOS':  'BOS',
        'CHA':  'CHA',
        'CHI':  'CHI',
        'CLE':  'CLE',
        'DAL':  'DAL',
        'DEN':  'DEN',
        'DET':  'DET',
        'GSW':  'GS',
        'HOU':  'HOU',
        'IND':  'IND',
        'LAC':  'LAC',
        'LAL':  'LAL',
        'MEM':  'MEM',
        'MIA':  'MIA',
        'MIL':  'MIL',
        'MIN':  'MIN',
        'NOP':  'NO',
        'NYK':  'NY',
        'OKC':  'OKC',
        'ORL':  'ORL',
        'PHI':  'PHI',
        'PHX':  'PHO',
        'POR':  'POR',
        'SAC':  'SAC',
        'SAS':  'SA',
        'TOR':  'TOR',
        'UTA':  'UTA',
        'WAS':  'WAS',
        }
    h=convert[home]
    v=convert[visitor]

    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBATeams"

    querystring = {"schedules":"true","rosters":"true"}


    key = 'c25bdc2c24msh8b9b73d7c986ea0p1a2cc1jsn7aaf7636b342'
    
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }
    seconds = 0
    teamStats = load_obj('teamStats')
    response = []
    #team data cache dont request api if already have recent info...
    try:
        lastupdate = teamStats['lastupdate']
        now = datetime.now()
        time_diff = now-lastupdate
        seconds = time_diff.total_seconds()
        print('Seconds since last update',seconds)
    except KeyError:
        print('no saved team stats found')
        teamStats = {}
    if seconds == 0 or seconds>1800:
        print('getting updated results')

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        lastupdate = datetime.now()
        teamStats['response']=response
        teamStats['lastupdate']=lastupdate
        save_obj(teamStats,'teamStats')
    else:
        print('loaded cached results')
        response = teamStats['response']
    r = response['body']
    teamStats = {}
    #complex injury data
    for team in range(len(r)):
        print(r[team]['teamAbv'])
        steak = r[team]['currentStreak']['result']
        steakLength = r[team]['currentStreak']['length']
        if steak == 'L':
            steakLength = int(steakLength) * -1
        W = r[team]['wins']
        L = r[team]['loss']
        GP = int(W)+int(L)
        c = 0
        injuries = []
        injuriesComplex = []
        for player in r[team]['Roster']:
            if r[team]['Roster'][player]['injury']['injDate'] != '':
                c+=1
                #print(r[team]['Roster'][player]['injury']['injDate'])
                #print(r[team]['Roster'][player]['nbaComName'])
                d = r[team]['Roster'][player]['injury']['description']
                if len(r[team]['Roster'][player]['injury']['description']) < 5:
                    d= "No Description"
                foo = [r[team]['Roster'][player]['nbaComName'],d,r[team]['Roster'][player]['injury']['injDate'],r[team]['Roster'][player]['injury']['designation']]
                injuriesComplex.append(foo)

                injuries.append(r[team]['Roster'][player]['nbaComName'])
        teamStats.update({r[team]['teamAbv']:[GP,W,L,steakLength,injuries,injuriesComplex]})

    #print(teamStats)
    #save_obj(teamStats,"teamStats")
        
    #return team stats
    return [teamStats[h],teamStats[v]]

# gets spread data from several books
# takes home and visitor abv, and date
# returns ['homeTeamSpread'],'awayTeamSpread',spread]
def getSpread(home,visitor,date):
    print('date--------',date)
    date = date.replace('-', '')
    #convert api abv
    convert = {
        'ATL' :'ATL',
        'BKN':  'BKN',
        'BOS':  'BOS',
        'CHA':  'CHA',
        'CHI':  'CHI',
        'CLE':  'CLE',
        'DAL':  'DAL',
        'DEN':  'DEN',
        'DET':  'DET',
        'GSW':  'GS',
        'HOU':  'HOU',
        'IND':  'IND',
        'LAC':  'LAC',
        'LAL':  'LAL',
        'MEM':  'MEM',
        'MIA':  'MIA',
        'MIL':  'MIL',
        'MIN':  'MIN',
        'NOP':  'NO',
        'NYK':  'NY',
        'OKC':  'OKC',
        'ORL':  'ORL',
        'PHI':  'PHI',
        'PHX':  'PHO',
        'POR':  'POR',
        'SAC':  'SAC',
        'SAS':  'SA',
        'TOR':  'TOR',
        'UTA':  'UTA',
        'WAS':  'WAS',
        }
    #h=convert[home]
    #v=convert[visitor]

    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBABettingOdds"

    querystring = {"gameDate": date}

    headers = {
        "X-RapidAPI-Key": "c25bdc2c24msh8b9b73d7c986ea0p1a2cc1jsn7aaf7636b342",
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    #spread cache system
    seconds = 0
    spreadCache = {}
    spreadCache = load_obj('spreadCache')
    response = []
    try:
        lastupdate = spreadCache['lastupdate']
        cacheDate = spreadCache['date']
        now = datetime.now()
        time_diff = now-lastupdate
        seconds = time_diff.total_seconds()
        print('Seconds since last spread update',seconds)
    except KeyError:
        print('no saved spread found')
        spreadCache = {}
    if seconds == 0 or seconds>60 or date != cacheDate:
        print('getting updated spread odds')
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        lastupdate = datetime.now()
        spreadCache['response']=response
        spreadCache['lastupdate']=lastupdate
        spreadCache['date'] = date
        save_obj(spreadCache,'spreadCache')
    else:
        print('loaded cached spread')
        response = spreadCache['response']
    r = response['body']

    print(r)
    if len(r) < 1:
        return ['0','0']
    spread = {}
    books = ['fanduel','wynnbet','caesars_sportsbook','betmgm','unibet','pointsbet','betrivers','sports_illustrated']
    for line in r:
        teams = line.split('_')[1].split('@')
        print(teams)
        if teams[0] == convert[home] or teams[1] == convert[home]:
            if teams[0] == convert[visitor] or teams[1] == convert[visitor]:

                for book in books:

                    spread[book] = {}
                    try:
                        spread[book]['homeTeamSpread']=r[line][book]['homeTeamSpread']
                        spread[book]['awayTeamSpread']=r[line][book]['awayTeamSpread']
                        spread[book]['homeTeamMLOdds']=r[line][book]['homeTeamMLOdds']
                        spread[book]['awayTeamMLOdds']=r[line][book]['awayTeamMLOdds']
                        spread[book]['totalUnder']=r[line][book]['totalUnder']
                        spread[book]['totalOver']=r[line][book]['totalOver']

                    except KeyError:
                        spread[book]['homeTeamSpread']=0
                        spread[book]['awayTeamSpread']=0
                        spread[book]['homeTeamMLOdds']=0
                        spread[book]['awayTeamMLOdds']=0
                        spread[book]['totalUnder']=0
                        spread[book]['totalOver']=0
                print('complex spread report:',spread)

                '''

                print(r[line]['fanduel']['homeTeamSpread'])
                print(r[line]['wynnbet']['homeTeamSpread'])
                print(r[line]['caesars_sportsbook']['homeTeamSpread'])
                print(r[line]['betmgm']['homeTeamSpread'])
                

                '''
                #return bets
                return [r[line]['fanduel']['homeTeamSpread'],r[line]['fanduel']['awayTeamSpread'],spread]


# Predict future game, this the main web predict function...
# returns found, gameid, and playerids
def futureGame(spread,homeTeamStats,visitorTeamStats,date,homeAbv,visitorAbv,path, season,labels,removed_players):
    print('removed player:',removed_players)
    print(season)
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    url+=date
    response = req(url)#request api for game
    nOsTAtsYET = {}
    found = False
    gameid = 0
    playerids = []
    for game in range(len(response['data'])):#find game in response
        ha = response['data'][game]['home_team']['abbreviation']
        va = response['data'][game]['visitor_team']['abbreviation']
            
        if ha==homeAbv and va==visitorAbv:#found game
            print('found--------123-------')
            found = True
            gameid = response['data'][game]['id']#set game id
            data = nextGame(gameid)
            #set team ids
            homeTeamID = str(response['data'][game]['home_team']['id'])
            visitorTeamID = str(response['data'][game]['visitor_team']['id'])
            #create data object
            data.update({'home_team_id':response['data'][game]['home_team']['id']})
            data.update({'visitor_team_id':response['data'][game]['visitor_team']['id']})
            data.update({'home_team_score' : response['data'][game]['home_team_score']})
            data.update({'visitor_team_score' : response['data'][game]['home_team_score']})
            

            #load team player rosters and season averages
            playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
            seasonAverages = load_obj('2022SeasonAverages')
 
            #get all home players
            homePlayers = []
            for player in playerIdByTeamID[homeTeamID]:
                if str(player) not in removed_players:
                    homePlayers.append(player)
                else:
                    print('found removed player ', player)
            #get all visitor players
            visitorPlayers = []
            for player in playerIdByTeamID[visitorTeamID]:
                if str(player) not in removed_players:
                    visitorPlayers.append(player)
                else:
                    print('found removed player ', player)


            homeTeam = []
            visitorTeam = []
            #get home team season averages
            for id in homePlayers:
                if player not in removed_players:
                    homeTeam.append(seasonAverages[id])
                else:
                    print('removed player: ', id)
            #get visitor team season averages
            for id in visitorPlayers:
                if player not in removed_players:
                    visitorTeam.append(seasonAverages[id])
                else:
                    print('removed player: ', id)


            #get home team top 7 players by play time
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
            #get visitor team top 7 players by play time
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








            hlastID = getLastGame(homeTeamID,date)
            vlastID = getLastGame(visitorTeamID,date)
            print(hlastID,vlastID,'----------+++-------')

            hurl = 'https://www.balldontlie.io/api/v1/stats?game_ids[]='+str(hlastID)+'&per_page=100'
            hLastGame = req(hurl)
            vurl = 'https://www.balldontlie.io/api/v1/stats?game_ids[]='+str(vlastID)+'&per_page=100'
            vLastGame = req(vurl)



            home_history = formLastGame(hLastGame,homeTeamID)
            visitor_history = formLastGame(vLastGame,visitorTeamID)



            #print best players
            print('visitor team:',len(bestV),bestVisitorIds) 
            print('home team:',len(bestH),bestHomeIds) 
            #write csv header
            writeCSVHeader(labels, path)
            #write game input data to csv
            writeCSV(spread,homeTeamStats,visitorTeamStats,gameid,homeTeamID,visitorTeamID,bestH,bestV,path,home_history,visitor_history)
            #return all the players ids we used to make game
            playerids = bestHomeIds+bestVisitorIds
    return found,gameid,playerids,hlastID,vlastID,json.dumps(home_history),json.dumps(visitor_history)
#------------------------------------------------------------------------#








def formLastGame(data,team):
    print('forming last game data')
    if data is None or len(data)<1:
        print('no ata=---------=========------------==========')
        return ''
    if int(data['data'][0]['game']['home_team_id']) == int(team):
        history_id = data['data'][0]['game']['home_team_id']
        opponent_id = data['data'][0]['game']['visitor_team_id']
        history_score = data['data'][0]['game']['home_team_score']
        opponent_score = data['data'][0]['game']['visitor_team_score']
    else:
        opponent_id = data['data'][0]['game']['home_team_id']
        history_id = data['data'][0]['game']['visitor_team_id']
        opponent_score = data['data'][0]['game']['home_team_score']
        history_score = data['data'][0]['game']['visitor_team_score']
    game_date = data['data'][0]['game']['date']
    gameid = data['data'][0]['game']['id']

    opponent_players = []
    history_players = []
    
    for player in  data['data']:
        p = {}
        p['id'] = player['player']['id']
        p['teamid'] = player['team']['id']
        print(player)
        for label in labels:
            if player['min'] is None:
                continue
            if label == 'min':
                min = player['min']
                min = min.split(':')[0]
                player['min']=min
            if player[label] is None:
                p[label] = 0
                continue
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
    return[best_history_players,best_opponent_players,history_score,opponent_score,gameid,opponent_id,game_date]


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
        if int(min) >= int(topMin):
            best = player
            topMin = min
    return best





def getLastGame(teamid, date):
    format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'  # Format for parsing game dates

    # Convert from string format to datetime format
    inputDate = datetime.strptime(date, format)
    
    today = inputDate - timedelta(days=360)
    start = today.strftime("%Y-%m-%d")
    today = inputDate - timedelta(days=1)
    end = today.strftime("%Y-%m-%d")
    url = f'https://www.balldontlie.io/api/v1/games?start_date={start}&end_date={end}&team_ids[]={teamid}&per_page=100'

    r = req(url)  # Using your original request function
    games = r['data']
    games.reverse()

    closest_game_1 = None
    closest_game_2 = None
    closest_diff_1 = timedelta.max
    closest_diff_2 = timedelta.max

    for game in games:
        # Skip games without scores
        if int(game['home_team_score']) == 0 or int(game['visitor_team_score']) == 0:
            continue

        game_date = datetime.strptime(game['date'], datetime_format)
        diff = abs(inputDate - game_date)

        if diff < closest_diff_1:
            closest_game_2, closest_diff_2 = closest_game_1, closest_diff_1
            closest_game_1, closest_diff_1 = game, diff
        elif diff < closest_diff_2:
            closest_game_2, closest_diff_2 = game, diff

    lastID = closest_game_1['id'] if closest_game_1 else None
    lastID2 = closest_game_2['id'] if closest_game_2 else None

    return lastID


# write indevidual csv file for game prediction
def writeCSV(spread,homeTeamStats,visitorTeamStats,game,homeId,visitorId,bestH,bestV,path,home_history,visitor_history):
    line = str(game)+','+str(spread)+','+str(homeId)
    for stat in homeTeamStats:#win/loss/streak
        line+=','+str(stat)
    line += ','+str(visitorId)
    for stat in visitorTeamStats:#win/loss/streak
        line+=','+str(stat)
    for player in range(len(bestH)):#best players
        for stat in range(len(bestH[player])):
            line += ','+str(bestH[player][stat])
    for player in range(len(bestV)):#best players
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




    
    csv = open(path,'a')#open csv
    csv.write(line+'\n')#write line
    print(line)
# write csv header
def writeCSVHeader(labels, path,**kwargs):
    header = 'gameid,spread,home_id,home_streak,hgp,hw,hl,visitor_id,visitor_streak,vgp,vw,vl'
    derp = ['home_', 'visitor_']
    for foo in derp:#home vistor
        for i in range(0,playersPerTeam):#0-6
            for label in labels:
                header+=','+foo+str(i)+'_'+label#make lables


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


    #write header
    csv = open(path,'w')
    csv.write(header+'\n')
    return header

#------------------------------------------------------------------------#
# get best player by play time
# takes team list of season averages
# returns best
def getBestPlayer(team):
    best = ''
    topMin = 0
    for player in range(len(team)):#for player on team

        if len(team[player]) == 0:#skip 0 min players
            continue
        min = team[player][-1]#set current player min
        min = min.split(':')[0]#convert to minute value from 20:32 to 20
        #print(min,topMin)
        if int(min) >= int(topMin):#is this player better then top players
            best = player#set new best
            topMin = min#set new best minute value
    return best#return best


#------------------------------------------------------------------------#


# clears data of last game and gets ready for next
# dont think this used anymore
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

#------------------------------------------------------------------------#
#request a url
# used to need proxies due to request getting blocked
# but nolonger using proxies, just makes request and returns json obj
def req(url):
    proxy = load_obj('proxy')#load proxies
    dict = {}
    p = random.randint(0,len(proxy)-1)#get random proxy
    dict.update({'http' : proxy[p]})
    r = requests.get(url)#request url
    print('proxy: ', proxy[p], 'url: ', url, 'response: ', r)
    if str(r) != '<Response [200]>':#means we request too fast
        time.sleep(5)#wait 5 seconds
        req(url)
    return r.json()
#------------------------------------------------------------------------#
#saves pickle object file
def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#loads pickle object file
def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#------------------------------------------------------------------------#
# Loads tensorflow model and predicts game
# Takes model number path of csv file and username
# returns prediction 
def predict(modelNum,path,username):
    #read csv file and cread pandas df
    data = pd.read_csv(path)
    #load model settings
    try:
        modelSettings = load_obj(str(username.username)+'ModelSettings'+modelNum)
    except FileNotFoundError:
        modelSettings = load_obj('DefaultModelSettings')
    #drop a bunch of values

    d = ['gameid','home_id','visitor_id','home_history_gameid','visitor_history_gameid']
    try:
        if modelSettings['streaks'] != 'true':
            d=d+['home_streak','visitor_streak']
        if modelSettings['wl'] != 'true':
            d=d+['hw','hl','vw','vl']
        if modelSettings['gp'] != 'true':
            d=d+['hgp','vgp']
        if modelSettings['ps'] != 'true':
            d.append('spread')
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for currentPlayer in range(int(modelSettings['players']),7):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        stat = foo+str(currentPlayer)+'_'+label#make lables
                        d.append(stat)

        features = ['min']
        if modelSettings['ast'] == 'true':
            features.append('ast')
        if modelSettings['blk'] == 'true':
            features.append('blk')
        if modelSettings['reb'] == 'true':
            #features.append('reb')
            features.append('dreb')
            features.append('oreb')
        if modelSettings['fg3'] == 'true':
            #features.append('fg3_pct')
            features.append('fg3m')
            features.append('fg3a')
        if modelSettings['fg'] == 'true':
            features.append('fga')
            features.append('fgm')
        if modelSettings['ft'] == 'true':
            features.append('fta')
            features.append('ftm')
        if modelSettings['pf'] == 'true':
            features.append('pf')
        if modelSettings['pts'] == 'true':
            features.append('pts')
        if modelSettings['stl'] == 'true':
            features.append('stl')
        if modelSettings['turnover'] == 'true':
            features.append('turnover')
        

        for currentPlayer in range(0,int(modelSettings['players'])):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        if label not in features:
                            stat = foo+str(currentPlayer)+'_'+label#make labels
                            d.append(stat)
    except KeyError:
        d = ['gameid','home_id','visitor_id','home_streak','visitor_streak','hgp','hw','hl','vgp','vw','vl']
    data.drop(d, axis=1, inplace=True)

    #convert data to values
    data = data.values
    #convert values to floats
    data = data.astype(float)


    #x_train = tf.keras.utils.normalize(x_train, axis=1)
    #x_test = tf.keras.utils.normalize(x_test, axis=1)


    #define squential model
    model = tf.keras.Sequential([

    tf.keras.layers.Dense(modelSettings['layer1Count'], activation=modelSettings['layer1Activation']),
    tf.keras.layers.Dense(modelSettings['layer2Count'], activation=modelSettings['layer2Activation']),
    tf.keras.layers.Dense(2, activation='linear'),

    ])
    #compile model
    model.compile(optimizer=modelSettings['optimizer'], loss='mean_squared_error', metrics=['accuracy'])
    #load model weights
    try:
        modelSettings = load_obj(str(username.username)+'ModelSettings'+modelNum)
        model.load_weights('./userModels/'+username.username+'/'+modelNum+'/checkpoints/my_checkpoint')
    except FileNotFoundError:
        model.load_weights('./checkpoints/my_checkpoint')

    #make prediction
    p = model.predict(data)
    return(p[0])


# request for spread api
def reqSpread(url):
    r = requests.get(url)
    return r.json()
