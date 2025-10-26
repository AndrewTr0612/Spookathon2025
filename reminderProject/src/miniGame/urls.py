from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_home, name='game_home'),
    path('buy-water/', views.buy_water, name='buy_water'),
    path('water-plant/', views.water_plant, name='water_plant'),
    path('stats/', views.game_stats, name='game_stats'),
]
