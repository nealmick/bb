import requests,random





def reqSpread(url):
    r = requests.get(url)
    return r.json()



def getSpread(h,v):
    keys = ['f003fe2f0e443e7bfece9c357b90c20d',
            'ea5ba76fd8807efa3b484121888f0f70',
            'ccd995270783b8fd83bef5a433877e9f',
            '790780270afebabec377041febe25c8a',
            '463ef39f21a0ecba3cf87bcbd280fb2f'
    ]
    key = random.choice(keys)
    spreadURL = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds?markets=h2h,spreads,totals&regions=us&apiKey='+key
    print('spread url',spreadURL)
    CHOICES = {
    'ATL' :'Atlanta Hawks',
    'BKN':	'Brooklyn Nets',
    'BOS':	'Boston Celtics',
    'CHA':	'Charlotte Hornets',
    'CHI':	'Chicago Bulls',
    'CLE':	'Cleveland Cavaliers',
    'DAL':	'Dallas Mavericks',
    'DEN':	'Denver Nuggets',
    'DET':	'Detroit Pistons',
    'GSW':	'Golden State Warriors',
    'HOU':	'Houston Rockets',
    'IND':	'Indiana Pacers',
    'LAC':	'Los Angeles Clippers',
    'LAL':	'Los Angeles Lakers',
    'MEM':	'Memphis Grizzlies',
    'MIA':	'Miami Heat',
    'MIL':	'Milwaukee Bucks',
    'MIN':	'Minnesota Timberwolves',
    'NOP':	'New Orleans Pelicans',
    'NYK':	'New York Knicks',
    'OKC':	'Oklahoma City Thunder',
    'ORL':	'Orlando Magic',
    'PHI':	'Philadelphia 76ers',
    'PHX':	'Phoenix Suns',
    'POR':	'Portland Trail Blazers',
    'SAC':	'Sacramento Kings',
    'SAS':	'San Antonio Spurs',
    'TOR':	'Toronto Raptors',
    'UTA':	'Utah Jazz',
    'WAS':	'Washington Wizards',
    }
    h = CHOICES[h]
    v = CHOICES[v]
    spreadr = reqSpread(spreadURL)

    vistorSpread = 0
    homeSpread = 0
    dk_vistorSpread = 0
    dk_homeSpread = 0

    for provider in spreadr:
        for game in provider['bookmakers']:
            if game['title'] == 'FanDuel':
                if game['markets'][1]['outcomes'][0]['name'] == v and game['markets'][1]['outcomes'][1]['name'] == h:
                    print(game['markets'][1]['outcomes'][0])
                    vistorSpread = game['markets'][1]['outcomes'][0]['point']
                    homeSpread = game['markets'][1]['outcomes'][1]['point']
                    break
                if game['markets'][1]['outcomes'][0]['name'] == h and game['markets'][1]['outcomes'][1]['name'] == v:
                    print(game['markets'])

                    homeSpread = game['markets'][1]['outcomes'][0]['point']
                    vistorSpread = game['markets'][1]['outcomes'][1]['point']
                    break

    for provider in spreadr:
        for game in provider['bookmakers']:
            if game['title'] == 'DraftKings':
                if game['markets'][1]['outcomes'][0]['name'] == v and game['markets'][1]['outcomes'][1]['name'] == h:
                    print(game['markets'])

                    dk_vistorSpread = game['markets'][1]['outcomes'][0]['point']
                    dk_homeSpread = game['markets'][1]['outcomes'][1]['point']
                    break
                if game['markets'][1]['outcomes'][0]['name'] == h and game['markets'][1]['outcomes'][1]['name'] == v:
                    dk_homeSpread = game['markets'][1]['outcomes'][0]['point']
                    dk_vistorSpread = game['markets'][1]['outcomes'][1]['point']
                    break

    print(h,homeSpread,' - ',v,vistorSpread)
    return [homeSpread,vistorSpread,dk_homeSpread,dk_vistorSpread]

getSpread('BOS','CHA')
