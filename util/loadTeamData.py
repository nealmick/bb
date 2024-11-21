import pandas as pd
import pickle

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


teamids = load_obj("apiTeamIdsByAbv")
df = pd.read_excel('csv/Team-Data/2015-16/1-1-2015-16.xlsx')
f = df.to_dict()
num = ''
for x in range(len(f['TEAM_ID'])):
    if f['TEAM_ID'][x] == teamids['NOP']:
        num=x
        break
print(num)
print(f['GP'][num],f['W'][num],f['L'][num])
