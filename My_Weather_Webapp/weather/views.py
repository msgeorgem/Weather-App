from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
from .models import City, Lang
from .forms import CityForm
from .utils import TimestampConverter
from utilities.loading_json import DataLoader
from django.http import HttpResponse
from dotenv import load_dotenv
import os
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import sys
# from background_task import background

# Define a global variable
default_city = '756135'
closest_city = ''

# Create your views here.
def home(request):
    load_dotenv()
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    global default_city
    global closest_city
    city_id = ''

    if closest_city == '':
        city_id = default_city
    else:
        city_id = closest_city
    
    url = "http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric".format(city_id,SECRET_KEY)
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
    
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully!'
            message_class = 'is_success'
    
    form = CityForm()
    weather_data = []
    r = requests.get(url).json()
    print(r)
    city_weather = {
        'city' : r['city']['name'],
        'temperature' : r['list'][0]['main']['temp'],
        'feels_like' : r['list'][0]['main']['feels_like'],
        'temp_min' : r['list'][0]['main']['temp_min'],
        'temp_max' : r['list'][0]['main']['temp_max'],
        'sunrise' : TimestampConverter(r['city']['sunrise']).to_localdatetime(),
        'sunset' : TimestampConverter(r['city']['sunset']).to_localdatetime(),
        'description' : r['list'][0]['weather'][0]['description'],
        'icon' : r['list'][0]['weather'][0]['icon'],
        }
    weather_data.append(city_weather)
        
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request, 'weather/home.html', context)


def city_search(request):
    search_query = request.GET.get('search', '')
    locations = City.objects.filter(name__icontains=search_query)
    paginator = Paginator(locations, 15)  # Show 10 locations per page

    page_number = request.GET.get('page')
    locations = paginator.get_page(page_number)

    return render(request, 'locations/locations.html', {'locations': locations})



def development(request):
    load_dotenv()
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    city_id = '3081368'
    url = "http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric".format(city_id,SECRET_KEY)
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
    
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully!'
            message_class = 'is_success'
    
    form = CityForm()
    # cities = City.objects.get(id='2587183')
    weather_data = []
    # for city in cities:
    #     r = requests.get(url.format(city)).json()
    #     print(r)
    #     city_weather = {
    #         'city' : city.name,
    #         'temperature' : r['list'][0]['main']['temp'],
    #         'feels_like' : r['list'][0]['main']['feels_like'],
    #         'temp_min' : r['list'][0]['main']['temp_min'],
    #         'temp_max' : r['list'][0]['main']['temp_max'],
    #         'sunrise' : TimestampConverter(r['city']['sunrise']).to_localdatetime(),
    #         'sunset' : TimestampConverter(r['city']['sunset']).to_localdatetime(),
    #         'description' : r['list'][0]['weather'][0]['description'],
    #         'icon' : r['list'][0]['weather'][0]['icon'],
    #     }
    #     weather_data.append(city_weather)
    r = requests.get(url).json()
    print(r)
    city_weather = {
        'city' : r['city']['name'],
        'temperature' : r['list'][0]['main']['temp'],
        'feels_like' : r['list'][0]['main']['feels_like'],
        'temp_min' : r['list'][0]['main']['temp_min'],
        'temp_max' : r['list'][0]['main']['temp_max'],
        'sunrise' : TimestampConverter(r['city']['sunrise']).to_localdatetime(),
        'sunset' : TimestampConverter(r['city']['sunset']).to_localdatetime(),
        'description' : r['list'][0]['weather'][0]['description'],
        'icon' : r['list'][0]['weather'][0]['icon'],
        }
    weather_data.append(city_weather)
        
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request,'weather/development.html', context)
def delete_city(requests, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')






# def location_list(request):
#     # user_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
#     locations = City.objects.all()
#     return render(request, 'locations/location_list.html', {'locations': locations})

# def location_list_langs(request):
#     cities = City.objects.all().prefetch_related('langs')

#     city_langs = []
#     for city in cities:
#         city_langs.append({
#             'id': city.id,
#             'lon': city.lon,
#             'lat': city.lat,
#             'country': city.country,
#             'code': city.code,
#             'name': city.name,
#             'population': city.population,
#             'langs': [Lang.lang for Lang in city.langs.all()],
#             })
#     #   'langs': [lang.lang for lang in city.langs.all()] 

#     return render(request, 'locations/location_list.html', {'locations': city_langs})
#  below for html
# <td>{% for lang in location.langs %}{{ lang }}{% if not forloop.last %}, {% endif %}{% endfor %}</td> -->
# <p>Languages: {{ city.langs.all|join:", " }}</p>







def load_json(request):
    if request.method == 'POST':
        print('WTF')
        loader = DataLoader('I:/Mój dysk/PYTHON2023/Weather-App/My_Weather_Webapp/utilities/0current.city.list.json')
        loader.load_data()
        return HttpResponse('POST request received')
    else:
        return HttpResponse('GET request received')
    
def find_the_closest_city(request):
    if request.method == 'POST':
        print('WTF')
        
        return HttpResponse('POST request received')
    else:
        return HttpResponse('GET request received')

def reload(request):
    load_dotenv()
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    city_id = '3081368'
    url = "http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric".format(city_id,SECRET_KEY)
    
    message = ''
    message_class = ''
    
    weather_data = []
    r = requests.get(url).json()
    print(r)
    city_weather = {
        'city' : r['city']['name'],
        'temperature' : r['list'][0]['main']['temp'],
        'feels_like' : r['list'][0]['main']['feels_like'],
        'temp_min' : r['list'][0]['main']['temp_min'],
        'temp_max' : r['list'][0]['main']['temp_max'],
        'sunrise' : TimestampConverter(r['city']['sunrise']).to_localdatetime(),
        'sunset' : TimestampConverter(r['city']['sunset']).to_localdatetime(),
        'description' : r['list'][0]['weather'][0]['description'],
        'icon' : r['list'][0]['weather'][0]['icon'],
        }
    weather_data.append(city_weather)
        
    context = {
        'weather_data' : weather_data, 
        'message' : message,
        'message_class' : message_class
        }
    return render(request, 'weather/home.html', context)



@csrf_exempt
def development(request):
    load_dotenv()
    
    city_id = '3081368'
    
    err_msg = ''
    message = 'Your page is up and running smoothly. Enjoy browsing!'
    message_class = ''

    response = f'Python: {sys.version}<br>'
    response += '<br>'.join(sys.path)
  
    
    storage = {
        'dev_item_1' : settings.BASE_DIR,
        'dev_item_2' : f'Python: {sys.version}<br>',
        'dev_item_3' : '<br>'.join(sys.path)
    }
   
    print(message)
   
          
    context = {
        'storage' : storage, 
        'message' : message,
        'message_class' : message_class
        
        }
    if request.method == 'POST':
        print(request.POST)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        print(latitude, longitude, 'NICE')

        # response = f'Python: {sys.version}<br>'
        # response += '<br>'.join(sys.path)

    return render(request,'weather/development.html', context)


# @csrf_exempt
# def your_view(request):
#     if request.method == 'POST':
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')

#         print(latitude, longitude, 'NICE')

#         # Save to your model
#         # YourModel.objects.create(latitude=latitude, longitude=longitude)

#         return JsonResponse({'status': 'success'})
# def button_click_view(request):
#     long_running_task()
#     return HttpResponse('Task has been scheduled')

# @background(schedule=1)
# def long_running_task():
#     global default_city

#     # Your long running task goes here
#     print(default_city)
#     print(default_city)
#     print(default_city)
#     print(default_city)
#     print(default_city)
#     pass