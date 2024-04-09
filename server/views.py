from django.http import HttpResponse
from django.shortcuts import render
# import folium
from django.shortcuts import render, redirect
# Create your views here.

from .forms import ImageUploadForm
import json
import requests
from bs4 import BeautifulSoup

# import polyline
# import folium
# import requests


# def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
#     loc = "{},{};{},{};12,12;13,13;14,14".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
#     url = "http://router.project-osrm.org/route/v1/driving/"
#     r = requests.get(url + loc)
#     if r.status_code != 200:
    #     return {}
    # res = r.json()
    # routes = polyline.decode(res['routes'][0]['geometry'])
    # start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    # end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    # distance = res['routes'][0]['distance']

    # out = {'route': routes,
    #        'start_point': start_point,
    #        'end_point': end_point,
    #        'distance': distance
    #        }

    # return out
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/')  # Redirect to success page
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


def image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/')  # Redirect to success page
    return redirect('/')


def text(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/')  # Redirect to success page
    return redirect('/')


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/')  # Redirect to success page
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})


def fetch_OTP(request):
    try:
        url = request.GET.get('url')
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        description = soup.find('meta', attrs={'name': 'description'})['content']
        image_url = soup.find('meta', property='og:image')['content']
        return {'description': description, 'image_url': image_url}

    except Exception as e:
        print('Error in fetch_OTP func:', e)
        return None


# def showroute(request, lat1,long1,lat2,long2):
#     figure = folium.Figure()
#     lat1,long1,lat2,long2= 10, 10, 10, 11
#     route=get_route(long1,lat1,long2,lat2)
#     m = folium.Map(location=[(route['start_point'][0]),
#                                  (route['start_point'][1])],
#                        zoom_start=10)
#     m.add_to(figure)
#     folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
#     folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
#     folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)



    # lat1, long1, lat2, long2 = 10, 10, 11, 10
    # route = get_route(long1, lat1, long2, lat2)
    # folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    # folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
    # folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)



    # figure.render()
    # context={'map':figure}
    # return render(request,'showroute.html',context)
