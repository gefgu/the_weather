from django.shortcuts import render, get_object_or_404
import requests
from .models import City
from .forms import CityForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9426f14f9c66ae5af9513a6760935f0f'
    
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse("weather:index"))
        
    form = CityForm()
    
    cities = City.objects.all()
    
    weather_data = []
    message = ""
    
    for city in cities:
    
        r = requests.get(url.format(city)).json()
        
        try:
            city_weather = {
                "id" : city.id,
                "city": city.name,
                "temperature": r['main']['temp'],
                "description": r['weather'][0]['description'],
                "icon": r['weather'][0]['icon']
            }
        except Exception:
            city.delete()
            message = "Please Send a valid City Name"
            continue
        
        weather_data.append(city_weather)
        
    
    context = {"weather_data": weather_data, "form": form, "message": message}
    return render(request, 'weather/weather.html', context)


def delete(request, city_id):
    print(city_id)
    print(City.objects.all())
    city = get_object_or_404(City, pk=city_id)
    city.delete()
    return HttpResponseRedirect(reverse("weather:index"))
