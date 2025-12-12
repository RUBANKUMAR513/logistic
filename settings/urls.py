from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='settings_index'),
    path('list/', views.settings_list, name='settings_list'),
]
