from django.urls import include, path

from . import views
from .views import GameListView,GameCreateView,TodaysGamesCreate
urlpatterns = [
    #path('', GameListView.as_view(), name='home-predict'),
    path('new/', GameCreateView.as_view(), name='new-predict'),
    path('today/', TodaysGamesCreate.as_view(), name='predict-today'),
    path('edit/<int:pk>/', views.editGame, name='edit-predict'),
    path('edit/<int:pk>/<str:change>', views.saveEdit, name='save-edit'),

    path('', GameListView.as_view() , name='home-predict'),
    path('#<int:pk>', views.getScore , name='get-score'),
    #path('predicttoday/', views.predictToday , name='predict-today'),


]
