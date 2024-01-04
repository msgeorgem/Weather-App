from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name = 'home'),
    path('', views.reload, name = 'home'),
    path('locations/', views.city_search, name='locations'),

    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('load_json/', views.load_json, name='load_json'),
    # path('run-task/', views.button_click_view, name='button_click_view'),
    
    path('development/', views.development, name = 'development'),
]