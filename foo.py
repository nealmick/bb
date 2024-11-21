



import pickle


#save pkl object
def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#load pkl object
def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    


import time,requests,random

def req(url, max_retries=500):
    retries = 0
    time.sleep(3)

    while retries < max_retries:
        print(url)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            else:
                # Non-200 response, retry after waiting
                print(f'Received status code {r.status_code}. Retrying...')
                time.sleep(30)
        except requests.exceptions.ConnectionError as e:
            # Connection error, retry after waiting
            print('Connection error:', e)
            time.sleep(30)

        retries += 1
        print(f'Retry {retries}/{max_retries}')

    print('Maximum retries reached. Request failed.')
    return None
 



#seasons scanned for data
seasons = ['2010','2009','2008','2007','2006']
#reverse seasons so we start at older season
seasons.reverse()


def main(seasons,**kwargs):
    #return ''
    #iterate over seasons
    found = True
    for s in range(len(seasons)):
        season=seasons[s]
        games = load_obj(season+'Games')
        for game in games:
            if not found:
                print(game)
                if str(game) == '':
                    found = True
                else:
                    continue
            
            print(game)
            print(len(games[game]['data']))
            #print(games[game]['data'])
            url = 'https://www.balldontlie.io/api/v1/stats?&game_ids[]='+str(game)+'&per_page=100'
            response = req(url)
            games[game]['data']=response['data']
            save_obj(games, season+'Games')


main(seasons)