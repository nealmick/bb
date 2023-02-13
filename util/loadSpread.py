import pandas as pd
import pickle

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


teamids = load_obj("apiTeamIdsByAbv")
df = pd.read_excel('../Odds-Data-Clean/2007-08.xlsx')
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



'''

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
