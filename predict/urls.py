from django.urls import include, path

from . import views
from .views import GameListView,GameCreateView
urlpatterns = [
    #path('', GameListView.as_view(), name='home-predict'),
    path('new/', GameCreateView.as_view(), name='new-predict'),
    path('edit/<int:pk>/', views.editGame, name='edit-predict'),
    path('edit/<int:pk>/<str:change>', views.saveEdit, name='save-edit'),

    path('new/<str:home>/<str:visitor>/<str:date>/', views.quickcreate, name='quick-create'),

    path('', GameListView.as_view() , name='home-predict'),
    path('#<int:pk>/', views.getScore , name='get-score'),
    #path('predicttoday/', views.predictToday , name='predict-today'),


]
