#this script requests tank01 rapid nba api for spread data.
import requests
def getSpread(home,visitor):
    
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

    querystring = {"gameDate":"20230301"}

    headers = {
        "X-RapidAPI-Key": "c25bdc2c24msh8b9b73d7c986ea0p1a2cc1jsn7aaf7636b342",
        "X-RapidAPI-Host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    r = response['body']

    for line in r:
        teams = line.split('_')[1].split('@')
        if teams[0] == convert[home] or teams[1] == convert[home]:
            if teams[0] == convert[visitor] or teams[1] == convert[visitor]:
                return(r[line]['fanduel']['homeTeamSpread'])        


home_spread = getSpread('CHA','PHX')
visitor_spread = home_spread *-1
print(home_spread, visitor_spread)
