import json
from nba_api.stats.endpoints import TeamDashboardByTeamPerformance
from nba_api.stats.static import teams 



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



teams = teams.get_teams()
teamids = {}
for key in CHOICES:

    id = [x for x in teams if x['full_name'] == CHOICES[key]][0]
    id = id['id']
    teamids.update({key:id})


x = TeamDashboardByTeamPerformance(team_id=teamids['NOP'])
x = x.get_json()
x = json.loads(x)

for k in x:
    print(k,x[k])
    print('-----')
print('result set:',x['resultSets'][0]['rowSet'])
# dictionary

