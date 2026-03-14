from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('addmedicine/', views.addMedicine, name='addmedicine'),
    path('addstock/', views.addStock, name='addstock'),
    path('stockslist/', views.stocksList, name='stockslist'),
]
