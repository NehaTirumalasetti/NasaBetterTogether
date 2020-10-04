from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Nasa, Authentic
from geopy.geocoders import Nominatim
import json
from NLPScript import script

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        #add data to database
        print(request.POST.dict())
        nasa = Nasa()
        nasa.name = request.POST.get('name')
        nasa.email = request.POST.get('email')
        nasa.region = request.POST.get('region')
        nasa.eventType = request.POST.get('eventType')
        nasa.description = request.POST.get('description')
        nasa.save()    
        print(Nasa.objects.all())
       
        result, tweets_total = script(nasa.description)
        print('result'+str(result)+"tweet total="+str(tweets_total))

        if len(result) != 0:
            allLinks = ""
            for item in result:
                allLinks = allLinks + "," + item
            authentic = Authentic()
            authentic.name = request.POST.get('name')
            authentic.email = request.POST.get('email')
            authentic.region = request.POST.get('region')
            authentic.eventType = request.POST.get('eventType')
            authentic.description = request.POST.get('description')
            authentic.links = allLinks
            authentic.twitter = tweets_total
            authentic.save()
            print(Authentic.objects.all())

        return HttpResponseRedirect('/')
    return render(request, 'register.html')

def earth(request):
    return render(request, 'earth.html')

def world(request):
    return render(request, 'world.html')

def globe(request):
    cursor = Authentic.objects.all()
    all_locations = []
    for record in cursor:
        country = record.region
        links = record.links
        tweets = record.twitter
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(country)
        #print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        #json_obj = dict(x=location.latitude, y=location.longitude, country=country, links=links, tweets=tweets)
        #all_locations.append(json_obj)
        li = [location.latitude, location.longitude, country, links, tweets]
        all_locations.append(li)

    context = {"locations": all_locations}
    print(context) 
    return render(request, 'globe.html', context)