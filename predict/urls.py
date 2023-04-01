from django.urls import include, path

from . import views
from .views import GameListView
urlpatterns = [
    #path('', GameListView.as_view(), name='home-predict'),


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
    path('stats/', views.statsView , name='stats-view'),
    path('train/<str:model>', views.trainView , name='train-view'),
    path('makedataset', views.makeDataSet , name='make-dataset'),
    path('makedataset/<str:seasons>/<int:numgames>', views.makeDataSet , name='make-dataset'),
    path('trainmodel/<str:model>/<int:epochs>/<int:batchSize>/<int:layer1Count>/<str:layer1Activation>/<int:layer2Count>/<str:layer2Activation>/<str:optimizer>/<str:es>/<str:rmw>/<str:kr>', views.trainModel , name='train-model'),
    path('resetmodel/<str:model>', views.resetModel , name='reset-model'),
    path('faq/', views.faq , name='faq'),

]
