from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
from pytz import timezone
import webData
import webTrain

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


labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']



playersPerTeam = 7

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
def betsList(request):
    context = {}
    g = Game.objects.filter(author=request.user)
    g = g.filter(bet=True)
    g = g.filter(finished=True)
    count = 0
    total= -100
    min = -100
    for game in g:
        if game.ev_won == '1':
            count+=1
            total+=190.1
        else:
            total-=100
        if total < min:
            min=total






    context['numBets'] = len(g)
    context['correct'] = count
    context['totalSpent'] = len(g)*100
    context['totalWon'] = count*190
    context['totalProfit'] = count*190-len(g)*100
    context['total'] = total
    context['maxSpent'] = min

    context['p'] = round(count/len(g)*100)
    context['games'] = g
    return render(request,'predict/bets.html',context)

def setBet(request, pk):
    g = Game.objects.filter(pk=pk)
    bet = g.values('bet')[0]['bet']
    if bet:
        g.update(bet=False)
    else:
        g.update(bet=True)
    return redirect('edit-predict', pk)
def teamListView(request):
   
    context={}

    teamNamesbyID = load_obj('teamNamesbyID')
    teamAbvById = load_obj('teamAbvById')
    teamId = 0
    teams = []
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
        teams.append(team)

    context['teams'] = teams
    return render(request,'predict/teamList.html',context)

def teamView(request,abv):
    abv = abv.upper()
    print(abv)
    context={}

    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    teamNamesbyID = load_obj('teamNamesbyID')
    teamAbvById = load_obj('teamAbvById')
    teamId = 0
    for id in teamAbvById:
        if teamAbvById[id] == abv:
            teamId=id
    context['teamId'] = teamId
    teamName = teamNamesbyID[int(teamId)]
    players = playerIdByTeamID[str(teamId)]
    print(len(players))
    p = []
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
        foo['avg'] = seasonAverages[player]
        foo['id'] = player
        data = getPlayerInfo(abv,foo['name'])
        foo['data'] = data 

        p.append(foo)


    context['p'] = p

    context['labels'] = labels





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




def updatePlayerTeam(request,playerId,**kwargs):
    print('updating team')
    url = 'https://www.balldontlie.io/api/v1/players/' + str(playerId)
    r = req(url)
    updatedId=str(r['team']['id'])
    savedId=0
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    for team in playerIdByTeamID:
        count=0
        for id in playerIdByTeamID[team]:
            if str(playerId) == str(id):
                savedId = team
                if int(savedId) != int(updatedId):
                    print('remove index:',count)
                    #uncomment to make this work, not tested as there are not trades to test....
                    playerIdByTeamID[team].pop(count)
                    playerIdByTeamID[updatedId].append(playerId)
            count+=1
    
    save_obj(playerIdByTeamID,'2022PlayerIdByTeamID')
    print('saved team id:',savedId)
    print('updated team id:',updatedId)
    
    return redirect('player-detail',playerId)

def updatePlayerStats(request,playerId,**kwargs):
    print('updating stats')
    seasonAverages = load_obj('2022SeasonAverages')
    url='https://www.balldontlie.io/api/v1/season_averages?player_ids[]='+str(playerId)
    r=req(url)
    res = []
    for label in labels:
        try:
            res.append(r['data'][0][label])
        except IndexError:
            return redirect('player-detail',playerId)

    seasonAverages[playerId] = res
    print(seasonAverages[playerId])
    save_obj(seasonAverages,'2022SeasonAverages')
    return redirect('player-detail',playerId)

def playerDetailbyName(request,key):
    obj = load_obj('2019PlayerNamesByID')
    player_id =''
    for id in obj:
        if obj[id].replace("'", "-") == key:
            print(id)
            player_id = id
            break

    return redirect('player-detail', player_id)
    


def playerDetail(request,playerId):
    context={}
    context['id'] = playerId
    context['labels'] = labels
    url = 'https://www.balldontlie.io/api/v1/players/' + str(playerId)
    r = req(url)
    print(r)
    
    context['weight_pounds'] = r['weight_pounds']
    context['height_feet'] = r['height_feet']
    context['height_inches'] = r['height_inches']
    context['position'] = r['position']
    context['conference'] = r['team']['conference']
    context['division'] = r['team']['division']
    context['abv'] = r['team']['abbreviation']

    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')
    teamNamesbyID = load_obj('teamNamesbyID')
    try:
        context['name'] = obj[str(playerId)]
    except KeyError:
        context['name'] = obj[int(playerId)]
        print('e')
    context['seasonAverage'] = seasonAverages[playerId]
    context['team'] = 0
    for team in playerIdByTeamID:
        for id in playerIdByTeamID[team]:

            if str(playerId) == str(id):
                context['team'] = team
                context['team_name'] = teamNamesbyID[int(team)]




    data = getPlayerInfo(context['abv'],context['name'])
    context['data']=data
    return render(request,'predict/playerDetail.html',context)

def getPlayerInfo(team,playerName):

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
    data = {}
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

def searchResults(request,playerName):
    context = {}
    context['playerName'] = playerName
    obj = load_obj('2019PlayerNamesByID')
    playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
    seasonAverages = load_obj('2022SeasonAverages')

    res = []
    for player in obj:
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
            res.append(p)
    context['res'] = res
    context['labels'] = labels

    return render(request,'predict/searchResults.html',context)


def playerSearch(request):
    context = {}
    return render(request,'predict/playerSearch.html',context)



def getAllScores(request):
    qs = Game.objects.filter(author=request.user)
    for instance in qs:
        print(instance.home_score)
        if int(instance.home_score)==0:
            time.sleep(1.3)
            getScore(request,instance.pk)
    return redirect('home-predict')




def faq(request):

    return render(request,'predict/faq.html')


@login_required
def resetModel(request,model):
    if os.path.exists("userModels/"+str(request.user.username)+'/'+model+'/'):
        shutil.rmtree("userModels/"+str(request.user.username)+'/'+model+'/')
        os.remove("updatedObj/"+str(request.user.username) +"ModelSettings"+model+".pkl")

    return redirect('train-view',model)

@login_required
def trainView(request,model):
    context = {}
    context['model'] = model
    username = request.user
    try:
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
        except KeyError:
            context['es']='true'
            context['rmw']='true'
            context['kr']='true'
    except FileNotFoundError:
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
        except KeyError:
            context['es']='true'
            context['rmw']='true'
            context['kr']='true'
        
    return render(request,'predict/train.html',context)

@login_required
def makeDataSet(request,seasons,numgames):
    print(seasons,numgames)
    seasons = seasons.split('-')
    print(seasons)
    webData.CreateDataset(seasons,numgames)
    return redirect('train-view')
@login_required
def trainModel(request,model,epochs,batchSize,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,es,rmw,kr):
    username = request.user
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

    results = webTrain.webappTrain(model,epochs,size,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,username,es,rmw,kr)
    modelSettings['results']=results[0]
    modelSettings['eval']=results[1]
    save_obj(modelSettings,str(username.username)+'ModelSettings'+model)

    context['showresults'] = True
    context['results'] = results[0]
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
    eval = modelSettings['eval']
    context['eval'] = eval
    return render(request,'predict/train.html',context)

@login_required
def statsView(request):
    context = {}
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

    return render(request,'predict/stats.html',context)

def removePlayer(request,pk,player):
    print(pk)
    print(player)
    obj = load_obj('2019PlayerNamesByID')
    player_id =''
    for id in obj:
        if obj[id].replace("'", "-") == player:
            print(id)
            player_id = id
            break

    g = Game.objects.filter(pk=pk)

    home = g.values('home')[0]['home']
    visitor = g.values('visitor')[0]['visitor']
    csvid = g.values('csvid')[0]['csvid']
    date = g.values('gamedate')[0]['gamedate']

    removed_players=g.values('removed_players')[0]['removed_players']
    date=g.values('gamedate')[0]['gamedate']

    if removed_players is not None:
        removed_players = json.loads(removed_players)
        removed_players.append(str(player_id))
    else:
        removed_players = []
        removed_players.append(str(player_id))
    removed_players_dump = json.dumps(removed_players)
    season = '2022'
    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
    path = 'csv/'+str(request.user)+str(csvid)+'.csv'







    spread = getSpread(home,visitor,date)
    home_spread = spread[0]
    visitor_spread = spread[1]

    stats = getTeamData(home,visitor)
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
    found, gameid, playerids = futureGame(home_spread,homeTeamStats,visitorTeamStats,date,home,visitor,path,season,labels,removed_players)


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
    g.update(author=request.user,home=home,visitor=visitor,gamedate=date,homecolor=TEAMCOLORS[home],visitorcolor=TEAMCOLORS[visitor],csvid=csvid,
        p0 = playerids[0], p1 = playerids[1], p2 = playerids[2], p3 = playerids[3], p4 = playerids[4], p5 = playerids[5],
        p6 = playerids[6], p7 = playerids[7], p8 = playerids[8], p9 = playerids[9], p10 = playerids[10], p11 = playerids[11],
        p12 = playerids[12], p13 = playerids[13],
        gameid=gameid,home_spread=home_spread,visitor_spread=visitor_spread,dk_home_spread=home_spread,dk_visitor_spread=visitor_spread,
        home_games_won=homeTeamStats[1],home_games_loss=homeTeamStats[2],
        visitor_games_won=visitorTeamStats[1],visitor_games_loss=visitorTeamStats[2],home_streak=home_streak,visitor_streak=visitor_streak,
        homeInjury=homeInjury, visitorInjury=visitorInjury,removed_players=removed_players_dump,homeInjuryComplex=homeTeamInjuryComplex,visitorInjuryComplex=visitorTeamInjuryComplex)
    return redirect('edit-predict',pk)






def exportGames(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    header = ['gameid','gamedate','home','visitor','margin','spread_prediction','won_vs_spread','home_score','visitor_score','home_score_prediction','visitor_score_prediction','home_spread','visitor_spread','home_games_won','home_games_loss','visitor_games_won','visitor_games_loss','pmscore','home_injury','visitor_injury','removed_players']    
    
    writer = csv.writer(response)

    writer.writerow(header)
    user = request.user
    qs = Game.objects.filter(author=user)
    lines = []
    for game in qs:
        g = [game.gameid,game.gamedate,game.home,game.visitor,game.margin,game.spread_prediction,game.ev_won,game.home_score,game.visitor_score,
        game.home_score_prediction,game.visitor_score_prediction,game.home_spread,game.visitor_spread,
        game.home_games_won,game.home_games_loss,game.visitor_games_won,game.visitor_games_loss,game.pmscore,game.homeInjury,game.visitorInjury,game.removed_players]
        line = []
        for s in g:
            line.append(str(s))
        lines.append(line)

    for line in lines:
        writer.writerow(line)

    return response



def saveEdit(request,model,pk,change,**kwargs):

    model = str(model)
    username = request.user
    changes = change[7:].split('-')
    changes.pop(-1)
    print(changes)
    context = {}
    user = request.user
    g = Game.objects.filter(pk=pk)
    csvid = g.values('csvid')[0]['csvid']

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
            data = line
            break

    data = data.split(',')
    header= header.split(',')
    print(path,data,'-------')
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
    for c in changes:
        x = c.split(':')
        n=17*int(x[0])-17+int(x[1])
        data[n-2]=x[2]
        print(n)
        print(data[n-2])
    print(data,'fffffffffffff')


    writeCSVHeader(labels, path)
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
        f = open(path,'a')
        f.write(ss+'\n')
    w(data, path,g)  
    p = predict(model,path,username)
    print(p)

    #p = float(p[0])

    pmscore = float(p[0]-p[1])
    spread = float(g.values('home_spread')[0]['home_spread'])*-1
    margin = abs(spread-pmscore)
    print('spread ',g.values('home_spread')[0]['home_spread'],'pmscore ',p[0]-p[1])
    print('spread ',spread,'pmscore ',pmscore)
    if float(pmscore) < 0 and float(spread) < 0:
        print('both negative')
        #margin = pmscore+spread
    g.update(home_score_prediction=round(p[0],2))
    g.update(visitor_score_prediction=round(p[1],2))
    g.update(pmscore=p[0]-p[1])
    g.update(margin=abs(margin))
    g.update(model=model)
    spread = float(g.values('home_spread')[0]['home_spread'])*-1
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
    g.update(spread_prediction=pred)

    return redirect('home-predict')



##
def editGame(request,pk,**kwargs):
    context = {}
    user = request.user
    g = Game.objects.filter(pk=pk)
    csvid = g.values('csvid')[0]['csvid']
    gID = g.values('gameid')[0]['gameid']
    author = g.values('author')[0]['author']
    u = User.objects.filter(id=author).first()
    print('gID:', gID)

    if gID is None:
        return redirect('home-predict')
    def get_labels():
        lol= []
        ll = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for l in ll:
            lol.append(l.upper())
        return lol
    context['labels']= get_labels()
    context['asdf']= 'oof'

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
    #print(data,'ooooof')
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
    
    if g.values('visitor_score_prediction')[0]['visitor_score_prediction'] is not None:
        data.pop(0)
        header.pop(0)
        data.pop(0)
        header.pop(0)
    players = {}
    oofnog = []
    for i in range(0,14):
        #print(g.values('p'+str(i))[0]['p'+str(i)])
        oofnog.append(g.values('p'+str(i))[0]['p'+str(i)])
    url = 'https://www.balldontlie.io/api/v1/players/'
    resp = []
    #print(oofnog)
    for id in oofnog:
        obj = load_obj('2019PlayerNamesByID')
        #print(resp)
        found = False
        for x in obj:



            if int(x) == int(id):
                found = True
                print('found-------')
                resp.append(obj[x].replace("'", "-"))

        if not found:
            r = req(url+str(id))
            fn = r['first_name']
            ln = r['last_name']
            full = fn+' '+ln
            resp.append(full)
            obj.update({str(id) : full})
            save_obj(obj,'2019PlayerNamesByID')

    c = 0
    for oof in range(1,15):
        n=17*oof-17
        temp = [str(oof)]
        for f in range(n,n+17):
            temp.append(data[f])

        players.update({ resp[c] : temp })
        c+=1

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
    #print(players)

    return render(request, 'predict/edit.html',context)


def getScore(request,pk,**kwargs):
    print('b')
    print('getttttttttttting score')
    url = 'https://www.balldontlie.io/api/v1/games/'
    user= request.user
    g = Game.objects.filter(pk=pk).values('gameid')
    g = g[0]
    url += g['gameid']
    r = req(url)
    h = r['home_team_score']
    print('url====',url)

    v= r['visitor_team_score']
    print(request.user,'-----------------')
    p = Profile.objects.filter(user=request.user)
    po = Profile.objects.get(user=request.user)
    print(p.values('gain')[0]['gain'])
    if r['status'] == "Final":
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



        Game.objects.filter(pk=pk).update(finished=True)

    Game.objects.filter(pk=pk).update(home_score=h)
    Game.objects.filter(pk=pk).update(visitor_score=v)
    #print(pagenum)
    #x = redirect("home-predict")
    #return HttpResponsePermanentRedirect(reverse('home-predict') + "?page="+str(page_num))
    return redirect('home-predict')




def todaysGames(date):
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    eastern = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d'
    loc_dt = datetime.now(eastern)
    #naive_dt = datetime.now()
    url+=date
    print(url)
    r = req(url)
    games = []
    for game in range(len(r['data'])):
        habv = r['data'][game]['home_team']['abbreviation']
        hfn = r['data'][game]['home_team']['full_name']
        hscore = str(r['data'][game]['home_team_score'])
        vabv = r['data'][game]['visitor_team']['abbreviation']
        vfn = r['data'][game]['visitor_team']['full_name']
        vscore = str(r['data'][game]['visitor_team_score'])
        status = r['data'][game]['status']

        foo = {'habv':habv,'hfn':hfn,'hscore':hscore,'vabv':vabv,'vfn':vfn,'vscore':vscore,'status':status,'date':date}
        games.append(foo)
    if len(games)==0:
        games.append('No Games Today')
    return games




class GameListView(ListView, LoginRequiredMixin):
    model = Game
    template_name = 'predict/home.html'
    ordering = ['-date_posted']
    paginate_by = 20
    context_object_name = 'games'
    context = 'games'

    def get_context_data(self, **kwargs):
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
    def get_queryset(self, **kwargs):
        user = self.request.user
        return Game.objects.filter(author=user).order_by('-date_posted')

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




def predictAll(request,dateSelected,model,**kwargs):
    print(dateSelected)

    tg = todaysGames(dateSelected)
    print(tg)
    model = str(model)
    for game in tg:
        quickcreate(request,game['habv'],game['vabv'],game['date'])
        g = Game.objects.filter(author=request.user).order_by('-date_posted').first()
        saveEdit(request,model,g.pk,'',**kwargs)
        print('asdf')
    return redirect('home-predict')


def quickcreate(request,home,visitor,date):
    print('testing quick create---------------------')



    csvid = random.randint(1,100000)
    season = '2022'
    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
    path = 'csv/'+str(request.user)+str(csvid)+'.csv'







    spread = getSpread(home,visitor,date)
    print(spread)
    home_spread = spread[0]
    visitor_spread = spread[1]

    print('visitor spread==========',visitor_spread)
    stats = getTeamData(home,visitor)
    homeTeamStats = stats[0]
    homeTeamInjuryComplex = homeTeamStats.pop(-1)
    homeTeamInjury = homeTeamStats.pop(-1)
    visitorTeamStats = stats[1]
    visitorTeamInjuryComplex = visitorTeamStats.pop(-1)
    visitorTeamInjury = visitorTeamStats.pop(-1)
    
    home_streak = homeTeamStats.pop(-1)
    visitor_streak = visitorTeamStats.pop(-1)
    print('complex injury report',homeTeamInjuryComplex,visitorTeamInjuryComplex)
    homeTeamInjuryComplex = json.dumps(homeTeamInjuryComplex)
    visitorTeamInjuryComplex = json.dumps(visitorTeamInjuryComplex)
    removed_players = []
    found, gameid, playerids = futureGame(home_spread,homeTeamStats,visitorTeamStats,date,home,visitor,path,season,labels,removed_players)
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



    obj = Game.objects.create(author=request.user,home=home,visitor=visitor,gamedate=date,homecolor=TEAMCOLORS[home],visitorcolor=TEAMCOLORS[visitor],csvid=csvid,
        p0 = playerids[0], p1 = playerids[1], p2 = playerids[2], p3 = playerids[3], p4 = playerids[4], p5 = playerids[5],
        p6 = playerids[6], p7 = playerids[7], p8 = playerids[8], p9 = playerids[9], p10 = playerids[10], p11 = playerids[11],
        p12 = playerids[12], p13 = playerids[13],
        gameid=gameid,home_spread=home_spread,visitor_spread=visitor_spread,dk_home_spread=home_spread,dk_visitor_spread=visitor_spread,
        home_games_won=homeTeamStats[1],home_games_loss=homeTeamStats[2],
        visitor_games_won=visitorTeamStats[1],visitor_games_loss=visitorTeamStats[2],home_streak=home_streak,visitor_streak=visitor_streak,
        homeInjury=homeInjury, visitorInjury=visitorInjury,homeInjuryComplex=homeTeamInjuryComplex,visitorInjuryComplex=visitorTeamInjuryComplex)

    return redirect('edit-predict',obj.pk)
    #return redirect('home-predict')



def getTeamData(home,visitor):
    
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
        

    return [teamStats[h],teamStats[v]]

def getSpread(home,visitor,date):
    print('date--------',date)
    date = date.replace('-', '')
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
    for line in r:
        teams = line.split('_')[1].split('@')
        print(teams)
        if teams[0] == convert[home] or teams[1] == convert[home]:
            if teams[0] == convert[visitor] or teams[1] == convert[visitor]:
                print(r[line]['fanduel']['homeTeamSpread'])
                return [r[line]['fanduel']['homeTeamSpread'],r[line]['fanduel']['awayTeamSpread']]



def futureGame(spread,homeTeamStats,visitorTeamStats,date,homeAbv,visitorAbv,path, season,labels,removed_players):
    print('removed player:',removed_players)
    print(season)
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    url+=date
    response = req(url)
    nOsTAtsYET = {}
    found = False
    gameid = 0
    playerids = []
    for game in range(len(response['data'])):
        ha = response['data'][game]['home_team']['abbreviation']
        va = response['data'][game]['visitor_team']['abbreviation']
            
        if ha==homeAbv and va==visitorAbv:
            print('found--------123-------')
            found = True
            gameid = response['data'][game]['id']
            data = nextGame(gameid)
            
            homeTeamID = str(response['data'][game]['home_team']['id'])
            visitorTeamID = str(response['data'][game]['visitor_team']['id'])
            
            data.update({'home_team_id':response['data'][game]['home_team']['id']})
            data.update({'visitor_team_id':response['data'][game]['visitor_team']['id']})
            data.update({'home_team_score' : response['data'][game]['home_team_score']})
            data.update({'visitor_team_score' : response['data'][game]['home_team_score']})
            
            playerIdByTeamID = load_obj('2022PlayerIdByTeamID')
            seasonAverages = load_obj('2022SeasonAverages')
 


            homePlayers = []
            for player in playerIdByTeamID[homeTeamID]:
                if str(player) not in removed_players:
                    homePlayers.append(player)
                else:
                    print('found removed player ', player)
            visitorPlayers = []
            for player in playerIdByTeamID[visitorTeamID]:
                if str(player) not in removed_players:
                    visitorPlayers.append(player)
                else:
                    print('found removed player ', player)
            print(homePlayers,visitorPlayers)



            homeTeam = []
            visitorTeam = []

            for id in homePlayers:
                if player not in removed_players:
                    homeTeam.append(seasonAverages[id])
                else:
                    print('removed player: ', id)
            for id in visitorPlayers:
                if player not in removed_players:
                    visitorTeam.append(seasonAverages[id])
                else:
                    print('removed player: ', id)


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
            writeCSVHeader(labels, path)
            writeCSV(spread,homeTeamStats,visitorTeamStats,gameid,homeTeamID,visitorTeamID,bestH,bestV,path)

            #print('playerid by team-------------',playerIdByTeamID)

            #
            #playerids=writeCSV(data, path, labels)
            playerids = bestHomeIds+bestVisitorIds
    return found, gameid,playerids
#------------------------------------------------------------------------#

def writeCSV(spread,homeTeamStats,visitorTeamStats,game,homeId,visitorId,bestH,bestV,path):
    line = str(game)+','+str(spread)+','+str(homeId)
    for stat in homeTeamStats:
        line+=','+str(stat)
    line += ','+str(visitorId)
    for stat in visitorTeamStats:
        line+=','+str(stat)
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
    header = 'gameid,spread,home_id,home_streak,hgp,hw,hl,visitor_id,visitor_streak,vgp,vw,vl'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,playersPerTeam):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    return header

#------------------------------------------------------------------------#
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


#------------------------------------------------------------------------#


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



#------------------------------------------------------------------------#
def req(url):
    proxy = load_obj('proxy')
    dict = {}
    p = random.randint(0,len(proxy)-1)
    dict.update({'http' : proxy[p]})
    r = requests.get(url)
    print('proxy: ', proxy[p], 'url: ', url, 'response: ', r)
    if str(r) != '<Response [200]>':#means we request too fast..fast af boi so like anything under 1 r/sec cause error at 60 seconds in....
        time.sleep(5)
        req(url)
    #time.sleep(.1)
    return r.json()
#------------------------------------------------------------------------#
def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#------------------------------------------------------------------------#TensorFlow Time lets get it####################

def predict(modelNum,path,username):

    data = pd.read_csv(path)

    data.drop(['gameid','home_id','visitor_id','home_streak','visitor_streak','hgp','hw','hl','vgp','vw','vl'], axis=1, inplace=True)
    #data.drop(['home_streak'], axis=1, inplace=True)
    #data.drop(['visitor_streak'], axis=1, inplace=True)

    data = data.values
    data = data.astype(float)


    #x_train = tf.keras.utils.normalize(x_train, axis=1)
    #x_test = tf.keras.utils.normalize(x_test, axis=1)

    try:
        modelSettings = load_obj(str(username.username)+'ModelSettings'+modelNum)
    except FileNotFoundError:
        modelSettings = load_obj('DefaultModelSettings')


    model = tf.keras.Sequential([

    tf.keras.layers.Dense(modelSettings['layer1Count'], activation=modelSettings['layer1Activation']),
    tf.keras.layers.Dense(modelSettings['layer2Count'], activation=modelSettings['layer2Activation']),
    tf.keras.layers.Dense(2, activation='linear'),

    ])
        
    model.compile(optimizer=modelSettings['optimizer'], loss='mean_squared_error', metrics=['accuracy'])
    try:
        modelSettings = load_obj(str(username.username)+'ModelSettings'+modelNum)
        model.load_weights('./userModels/'+username.username+'/'+modelNum+'/checkpoints/my_checkpoint')
    except FileNotFoundError:
        model.load_weights('./checkpoints/my_checkpoint')

    p = model.predict(data)
    return(p[0])



def reqSpread(url):
    r = requests.get(url)
    return r.json()
