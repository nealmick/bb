#this script is used to load spread from saved csv dataset

import requests, json, time, operator, pickle, random
import pandas as pd
from datetime import datetime,timezone
seasons = ['2021']
seasons.reverse()
seasonsCSV = ['2021-22']
seasonsCSV.reverse()

labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
playersPerTeam = 7
path = "csv/train.csv"



def main(labels,seasons,**kwargs):
    print('asdf')
    for s in range(len(seasons)):
        season=seasons[s]
        seasonCSV=seasonsCSV[s]
        games = load_obj(season+'Games')
        teamNamesById = load_obj('teamNamesById')
        counter=0
        for game in games:
            g=games[game]
            try:
                print(g['spread'])
                continue
            except KeyError:
                print('getting spread')
            #print(game, g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])
            counter+=1
            df = pd.read_excel('Odds-Data-Clean/'+seasonCSV+'.xlsx')
            f = df.to_dict()
            d = datetime.fromisoformat(g['date'][:-1]).astimezone(timezone.utc)
            d = d.strftime('%m-%d')
            sc = 0
            found = False

            for x in range(len(f['Spread'])):  

                home = f['Home'][x]
                visitor = f['Away'][x]
                ml = f['ML_Home'][x]
                spread = f['Spread'][x]
                date = f['Date'][x]
                date = date.split('-')
                a = date[-1][0]+date[-1][1]
                b = date[-1][2]+date[-1][3]
                date = a+'-'+b
                if ml == 'NL':
                    print('bad game')
                elif int(ml) < 0:
                    spread = spread*-1
                if d == date:
                    print(seasonCSV,teamNamesById[g['visitor_id']],visitor)
                    if teamNamesById[g['visitor_id']] == visitor:
                        print('found game')
                        print(date,home,visitor,spread)
                        print(game, g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])
                        sc=spread
                        break
            print(game, g['winner'],g['date'],teamNamesById[g['home_id']],g['home_score'],teamNamesById[g['visitor_id']],g['visitor_score'])

            g['spread']=sc
            print(g['spread'])
            games[game]=g
            save_obj(games,season+'Games')
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
 
main(labels,seasons)
'''

games = load_obj('2021Games')

for game in games:
    g = games[game]
    print(g['spread'])

'''

'''


import pandas as pd
import pickle

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


df = pd.read_excel('../Odds-Data-Clean/2021-22.xlsx')
f = df.to_dict()
num = ''
print(f['Spread'])

for x in range(len(f['Spread'])):    
    home = f['Home'][x]
    visitor = f['Away'][x]
    ml = f['ML_Home'][x]
    spread = f['Spread'][x]
    date = f['Date'][x]
    #fix-date
    date = date.split('-')
    a = date[-1][0]+date[-1][1]
    b = date[-1][2]+date[-1][3]
    date = a+'-'+b
    if ml == 'NL':
        print('bad game')
    elif int(ml) < 0:
        spread = spread*-1
    print(date,home,visitor,spread)



    


    
used inside data.py to regather spread


            

            d = datetime.fromisoformat(g['date'][:-1]).astimezone(timezone.utc)
            d = d.strftime('%m-%d')
            s = 0
            for x in range(len(f['Spread'])):  

                home = f['Home'][x]
                visitor = f['Away'][x]
                ml = f['ML_Home'][x]
                spread = f['Spread'][x]
                date = f['Date'][x]
                date = date.split('-')
                a = date[-1][0]+date[-1][1]
                b = date[-1][2]+date[-1][3]
                date = a+'-'+b
                if ml == 'NL':
                    print('bad game')
                elif int(ml) < 0:
                    spread = spread*-1
                

                if d == date:
                    if teamNamesById[g['visitor_id']] == visitor:
                        print('found game')
                        print(date,home,visitor,spread)
                        print(game, g['winner'],g['date'],g['home_id'],g['home_score'],g['visitor_id'],g['visitor_score'])
                        s=spread
                

            g['spread']=s



'''
