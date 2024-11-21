from django.urls import include, path

from . import views
from .views import GameListView,GameListError
urlpatterns = [
    #path('', GameListView.as_view(), name='home-predict'),
    path('dash/', views.dash, name='dash'),

    path('ev/', views.ev, name='ev'),
    path('evrecord/', views.evRecord, name='ev-record'),
    
    path('history-arb/', views.arb_history, name='arb'),


    path('arb/', views.arb, name='arb'),

    path('arb/refresh/<str:region>', views.arbRefresh, name='arb-refresh'),

    path('update-arb/', views.update_arb, name='update_odds'),



    path('retrain-logs/<int:model>', views.retrainLogs, name='retrain-model'),

    path('retrain/<int:pk>', views.retrainModel, name='retrain-model'),

    path('clearstats/', views.clearStats, name='clear-stats'),
    path('cleargames/', views.clearGames, name='clear-games'),

    path('confirmcleargames/', views.confirmClearGames, name='confirm-clear-games'),

    path('updatespread/<int:pk>', views.updateSpread, name='update-spread'),
    path('bet/<int:pk>', views.setBet, name='bet'),
    path('bets/', views.betsList, name='bet-list'),
    path('bets/<str:team>/<int:days>', views.betsList, name='bet-list'),


    path('team/<str:abv>', views.teamView, name='team-view'),
    path('teams/', views.teamListView, name='team-list'),
    path('player-detail-name/<str:key>', views.playerDetailbyName, name='player-detail-name'),

    path('update-stats/<int:playerId>', views.updatePlayerStats, name='update-stats'),
    path('update-team/<int:playerId>', views.updatePlayerTeam, name='update-team'),

    path('player-details/<int:playerId>', views.playerDetail, name='player-detail'),
    path('player-search/', views.playerSearch, name='player-search'),
    path('player-search/<str:playerName>', views.searchResults, name='search-result'),
    path('getAllScores/', views.getAllScores, name='all-scores'),
    path('edit/<int:pk>/', views.editGame, name='edit-predict'),
    path('edit/<int:pk>/<int:model>/<str:change>', views.saveEdit, name='save-edit'),
    path('edit/<int:pk>/remove/<str:player>', views.removePlayer, name='remove-player'),

    path('new/<str:home>/<str:visitor>/<str:date>/', views.quickcreate, name='quick-create'),

    path('', GameListView.as_view() , name='home-predict'),
    path('date/<str:dateSelected>', GameListView.as_view() , name='home-predict'),
    path('all/', views.predictAll , name='predict-all'),
    path('all/<str:dateSelected>/<int:model>', views.predictAll , name='predict-all'),
    path('#<int:pk>', views.getScore , name='get-score'),
    path('#<int:pk>/<str:redirect>', views.getScore , name='get-score-edit'),
    path('stats/', views.statsView , name='stats-view'),
    path('train/<str:model>', views.trainView , name='train-view'),
    path('makedataset', views.makeDataSet , name='make-dataset'),
    path('makedataset/<str:seasons>/<int:numgames>', views.makeDataSet , name='make-dataset'),
    path('trainmodel/<str:model>/<int:epochs>/<int:batchSize>/<int:layer1Count>/<str:layer1Activation>/<int:layer2Count>/<str:layer2Activation>/<str:optimizer>/<str:es>/<str:rmw>/<str:kr>/<str:streaks>/<str:wl>/<str:gp>/<str:ps>/<str:players>/<str:ast>/<str:blk>/<str:reb>/<str:fg3>/<str:fg>/<str:ft>/<str:pf>/<str:pts>/<str:stl>/<str:turnover>/<str:re_eval>', views.trainModel , name='train-model'),
    path('resetmodel/<str:model>', views.resetModel , name='reset-model'),
    path('faq/', views.faq , name='faq'),
    path('usage/', views.usage , name='usage'),
    path('model-logs/<str:modelNum>/<str:lineNum>', views.modelLogs , name='model-logs'),

    path('all-model-logs/<str:modelNum>/', views.allModelLogs, name='all-model-logs'),
    path('props/', views.props, name='props'),
    path('tos-auth/', views.tos_auth, name='tos-auth'),



]
