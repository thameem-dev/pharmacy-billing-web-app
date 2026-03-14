from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('billentry/', views.billEntry, name='billentry'),
    path('salesreport/', views.SalesReport, name='salesreport'),
]
