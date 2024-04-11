from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm


import json
import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import os
import time


matplotlib.use('Agg')


def build_plot(data):
    names = [item['Name'] if len(item['Name']) < 12 else item['Name'][:12] + '...' for item in data]
    probs = [item['prob'] for item in data]

    colors = ['#d199ff', '#99e6ff', '#80ff80', '#ff9', '#ffc966']
    plt.bar(names, probs, color=colors)
    # plt.xlabel('Name')
    # plt.ylabel('Probability')
    # plt.title('Probability Distribution')
    plt.xticks(rotation=15)
    # plt.grid(True)

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
    # plt.show()
    # plt.savefig('../static')
    current_directory = os.getcwd()
    print("Текущая директория:", current_directory)
    plt.close()
    return img_base64


# build_plot([
#         {"XID": "W38411380", "Name": "Динамо", "kind": "sport", "city": None,  "OSM": "way/38411380", "WikiData": "Q37996725", "Rate": None, "Lon": 60.600349, "Lat": 56.845398, "prob": 0.5},
#         {"XID": "N2885181131", "Name": "№32 Дом обороны", "kind": "architecture", "city": None, "OSM": "node/2885181131", "WikiData": "Q55209768", "Rate": None, "Lon": 60.601315, "Lat": 56.834167, "prob": 0.3},
#         {"XID": "W38581890", "Name": "Дом обороны", "kind": "architecture", "city": None, "OSM": "way/38581890", "WikiData": "Q55209768", "Rate": None, "Lon": 60.602409, "Lat": 56.835133, "prob": 0.15},
#         {"XID": "N1930476141", "Name": "№28 Здание городской электростанции «Луч»", "kind": "architecture", "city": None, "OSM": "node/1930476141", "WikiData": "Q55154121", "Rate": None, "Lon": 60.60743, "Lat": 56.833691, "prob": 0.04},
#         {"XID": "N3002726097", "Name": "№27 Дом Г.Н. Скрябина", "kind": "architecture", "city": None, "OSM": "node/3002726097", "WikiData": "Q55232375", "Rate": None, "Lon": 60.607075	, "Lat": 56.834225, "prob": 0.01}
#     ])


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


# def index(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('/')  # Redirect to success page
#     else:
#         form = ImageUploadForm()
#     return render(request, 'index.html', {'form': form})

def custom_redirect(to):
    return redirect(to)


def fetch_OTP(request):
    try:
        url = request.GET.get('url')
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        description = soup.find('meta', attrs={'name': 'description'})['content']
        image_url = soup.find('meta', property='og:image')['content']
        return JsonResponse({'description': description, 'image_url': image_url})

    except Exception as e:
        print('Error in fetch_OTP func:', e)
        return JsonResponse({'error': 'Произошла ошибка при получении данных'}, status=500)
    

#ЗАГЛУШКА
def predict_photo(photo, city=None):
    result = [
        {"XID": "N6629818520", "Name": "Нижегородский кремль", "kind": "fortifications", "city": None,  "OSM": "node/6629818520", "WikiData": "Q1550905", "Rate": None, "Lon": 44.002522, "Lat": 56.328667, "prob": 0.5},
        {"XID": "N2885181131", "Name": "№32 Дом обороны", "kind": "architecture", "city": None, "OSM": "node/2885181131", "WikiData": "Q55209768", "Rate": None, "Lon": 60.601315, "Lat": 56.834167, "prob": 0.3},
        {"XID": "W38581890", "Name": "Дом обороны", "kind": "architecture", "city": None, "OSM": "way/38581890", "WikiData": "Q55209768", "Rate": None, "Lon": 60.602409, "Lat": 56.835133, "prob": 0.15},
        {"XID": "N1930476141", "Name": "№28 Здание городской электростанции «Луч»", "kind": "architecture", "city": None, "OSM": "node/1930476141", "WikiData": "Q55154121", "Rate": None, "Lon": 60.60743, "Lat": 56.833691, "prob": 0.04},
        {"XID": "N3002726097", "Name": "№27 Дом Г.Н. Скрябина", "kind": "architecture", "city": None, "OSM": "node/3002726097", "WikiData": "Q55232375", "Rate": None, "Lon": 60.607075	, "Lat": 56.834225, "prob": 0.01}
    ]
    return result


#ЗАГЛУШКА
def predict_text(text, city=None):
    result = [
        {"XID": "N6629818520", "Name": "Нижегородский кремль", "kind": "fortifications", "city": None,  "OSM": "node/6629818520", "WikiData": "Q1550905", "Rate": None, "Lon": 44.002522, "Lat": 56.328667, "prob": 0.5},
        {"XID": "N2885181131", "Name": "№32 Дом обороны", "kind": "architecture", "city": None, "OSM": "node/2885181131", "WikiData": "Q55209768", "Rate": None, "Lon": 60.601315, "Lat": 56.834167, "prob": 0.3},
        {"XID": "W38581890", "Name": "Дом обороны", "kind": "architecture", "city": None, "OSM": "way/38581890", "WikiData": "Q55209768", "Rate": None, "Lon": 60.602409, "Lat": 56.835133, "prob": 0.15},
        {"XID": "N1930476141", "Name": "№28 Здание городской электростанции «Луч»", "kind": "architecture", "city": None, "OSM": "node/1930476141", "WikiData": "Q55154121", "Rate": None, "Lon": 60.60743, "Lat": 56.833691, "prob": 0.04},
        {"XID": "N3002726097", "Name": "№27 Дом Г.Н. Скрябина", "kind": "architecture", "city": None, "OSM": "node/3002726097", "WikiData": "Q55232375", "Rate": None, "Lon": 60.607075	, "Lat": 56.834225, "prob": 0.01}
    ]
    return result


def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        description = soup.find('meta', attrs={'name': 'description'})['content']
        # img_url = soup.find('meta', property='og:image')['content']
        # img_response = requests.get(img_url)
        # img_base64 = base64.b64encode(img_response.content).decode('utf-8')
        return description
    except Exception as e:
        print('Error fetching content:', e)
        return None, None

def predict_image_frontend_bridge(data, city, isphoto):
    if isphoto:
        res = predict_photo(data, city)
    else:
        res = predict_text(data, city)

    for item in res:
        modal_url = 'https://opentripmap.com/ru/card/' + item['XID']
        # p_content = fetch_content(modal_url)
        p_content = 'empty'
        item['text_from_div'] = p_content
        # item['image_base64'] = img_base64

    return [{key: value for key, value in item.items() if key not in ['Rate', 'city']} for item in res]


def predict_image_api_bridge(request):
    if request.method == 'POST':
        city = request.POST.get('city', None)
        if city is None:
            if 'photo' in request.FILES:
                result = predict_photo(request.FILES['photo'])
            else:
                return JsonResponse({'error': 'Некорректный запрос'}, status=400)

        else:
            if 'photo' in request.FILES:
                result = predict_photo(request.FILES['photo'], city)
            else:
                return JsonResponse({'error': 'Некорректный запрос'}, status=400)
        
        # print("Поля в запросе:")
        # print(request.POST.keys())
        result =  [{key: value for key, value in item.items() if key not in ['OSM', 'WikiData', 'Rate']} for item in result]
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)
    

def predict_text_api_bridge(request):
    if request.method == 'POST':
        city = request.POST.get('city', None)
        if city is None:
            if 'text' in request.POST:
                result = predict_text(request.POST['text'])
            else:
                return JsonResponse({'error': 'Некорректный запрос'}, status=400)
        else:
            if 'text' in request.POST:
                result = predict_text(request.POST['text'], city)
            else:
                return JsonResponse({'error': 'Некорректный запрос'}, status=400)
        
        # print("Поля в запросе:")
        # print(request.POST.keys())
        result = sorted(result, key=lambda d: d['prob'], reverse=True)
        result = [{key: value for key, value in item.items() if key not in ['OSM', 'WikiData', 'Rate', "prob"]} for item in result]
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)


def predict_front(request):
    if request.method == 'POST':
        city = request.POST['city']
        # city = request.POST.get('city', None)
        if 'photo' in request.FILES:
            spots = predict_image_frontend_bridge(request.FILES['photo'], city, True)
        elif 'text' in request.POST:
            spots = predict_image_frontend_bridge(request.POST['text'], city, False)
        else:
            return JsonResponse({'error': 'Некорректный запрос'}, status=400)
        result = {}
        result['spots'] = spots
        # print(spots)
        result['image'] = build_plot(spots)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)


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
