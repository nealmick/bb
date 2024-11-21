import requests,pickle,random,time

def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#loads pickle object file
def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
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



url = 'https://www.balldontlie.io/api/v1/games?start_date=2023-03-20&end_date=2023-04-20&&team_ids[]=3&per_page=100'

r = req(url)
r = r['data']
print(type(r))
r.reverse()
lastID = None
for game in r:
    print(game['id'],game['date'],game['home_team_score'],game['visitor_team_score'],game['status'])
    if game['status'] == 'Final':
        lastID=game['id']
        break