import numpy as np
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# import folium
from django.shortcuts import render, redirect
# Create your views here.

from .forms import ImageUploadForm
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from rest_framework import viewsets
from .models import Places, Image, Category
from .serializers import PlacesSerializer, ImageSerializer, CategorySerializer
import ruclip
import torch
from model import OurModel
import warnings
import PIL
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import os
import time
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

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
class PlacesViewSet(viewsets.ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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

import random
def text(request):
    if request.method == 'POST':
        # form = ImageUploadForm(request.POST, request.FILES)
        # if form.is_valid():
        #     print(form.cleaned_data)
        #     form.save()
        ans = [{i.name: [i.XID, i.city]} for i in random.choices(Places.objects.all(), k=5)]
        print(ans)
        return JsonResponse({"places": ans}) # Redirect to success page
    return redirect('/')

model, processor = ruclip.load("ruclip-vit-base-patch16-384", device="cpu")
clf3 = torch.load("./clfs_nn(1).pth")
def predict_photo(photo, city):
    our_model = OurModel(model, processor, clfs=clf3, bs=5)
    img = PIL.Image.open(photo)
    res = our_model(city, images=[img])
    print(res, list(map(int, res.indices[0])))
    # places = Places.objects.filter(city=city, my_id__in=list(map(int, res.indices[0])))
    # places = Places.objects.all()[:5]
    category = dict()
    places = [Places.objects.get(city=city, name=our_model.showplaces_maping[city][res.indices[0][i].item()]) for i in
              range(len(res.indices[0]))]
    ans = []
    for j, i in enumerate(places):
        if i.name != 'nan':
            for kind in i.category.all():
                category[kind.name] = category.get(kind.name, 0) + float(res.values[0][j])
            ans.append(
                {"XID": i.XID, "Name": i.name, "Kind": [j.name for j in i.category.all()], "OSM": i.OSM, "Lon": i.Lon,
                 "Lat": i.Lat, "prob":(round(float(res.values[0][j]),4))})
    print(ans)
    top_5 = sorted(category, key=category.get, reverse=True)[:5]

    top_5_values = [category[key] for key in top_5]

    softmax_values = np.exp(top_5_values) / np.sum(np.exp(top_5_values))

    print("Топ 5 значений:")
    category_ans = []
    for place, value in zip(top_5, softmax_values):
        category_ans.append({place: value})
        print(f"{place}: {value}")
    print(category, softmax_values)
    # ans.append(category_ans)
    return ans


#ЗАГЛУШКА
def predict_text(request, city):
    print(city)
    our_model = OurModel(model, processor, clfs=clf3, bs=5)
    res = our_model(city, texts=[f'{request}'])
    print(res, list(map(int, res.indices[0])))
    # places = Places.objects.filter(city=city, my_id__in=list(map(int, res.indices[0])))
    # for i in range(len(res.indices[0])):
    #     print(our_model.showplaces_maping['NN'][res.indices[0][i].item()])
    #     print(Places.objects.get(name=our_model.showplaces_maping['NN'][res.indices[0][i].item()]))
    places = [ Places.objects.get(city=city, name=our_model.showplaces_maping[city][res.indices[0][i].item()]) for i in range(len(res.indices[0]))]
    ans  = []
    for j,i in enumerate(places):
        if i.name!= 'nan':
            ans.append({"XID": i.XID, "Name": i.name, "Kind":[j.name for j in i.category.all()],  "OSM": i.OSM,  "Lon": i.Lon, "Lat": i.Lat, "prob":(round(float(res.values[0][j]),4))})
    print(ans)
    return ans


from django.http import JsonResponse

# def predict_front(request):
#     if request.method == 'POST':
#         city = request.POST.get('city', "Нижний Новгород")
#         if 'photo' in request.FILES:
#             result = predict_photo(request.FILES['photo'], city)
#         elif 'text' in request.POST:
#             result = predict_text(request.POST['text'], city)
#         else:
#             return JsonResponse({'error': 'Некорректный запрос'}, status=400)
#         return JsonResponse(result, safe=False)
#     else:
#         return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)


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
        result = [{key: value for key, value in item.items() if key not in ['OSM', 'WikiData', 'Rate']} for item in
                  result]
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
        result = [{key: value for key, value in item.items() if key not in ['OSM', 'WikiData', 'Rate', "prob"]} for item
                  in result]
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=405)


def predict_front(request):
    if request.method == 'POST':
        city = request.POST.get('city', "Нижний Новгород")
        print(request.POST)
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

ctg_dict = {
"science_museums": "Научные музеи",
"other_temples": "Другие храмы",
"stadiums": "Стадионы",
"sport": "Спорт",
"cinemas": "Кинотеатры",
"other_technology_museums": "Другие технические музеи",
"museums_of_science_and_technology": "Музеи науки и техники",
"opera_houses": "Оперные театры",
"manor_houses": "Усадьбы",
"bank": "Банки",
"banks": "Банки",
"monasteries": "Монастыри",
"biographical_museums": "Биографические музеи",
"art_galleries": "Художественные галереи",
"national_museums": "Национальные музеи",
"other_burial_places": "Другие места захоронений",
"burial_places": "Места захоронений",
"tourist_facilities": "Туристические объекты",
"foods": "Еда",
"restaurants": "Рестораны",
"other_churches": "Другие церкви",
"eastern_orthodox_churches": "Восточно-православные церкви",
"churches": "Церкви",
"cathedrals": "Соборы",
"gardens_and_parks": "Сады и парки",
"mosques": "Мечети",
"religion": "Религия",
"kremlins": "Кремли",
"history_museums": "Исторические музеи",
"historic_districts": "Исторические районы",
"historical_places": "Исторические места",
"music_venues": "Места для музыкальных выступлений",
"theatres_and_entertainments": "Театры и развлечения",
"other_museums": "Другие музеи",
"museums": "Музеи",
"fortified_towers": "Укрепленные башни",
"fortifications": "Фортификации",
"other_towers": "Другие башни",
"towers": "Башни",
"monuments": "Памятники",
"sculptures": "Скульптуры",
"cultural": "Культурный",
"urban_environment": "Городская среда",
"monuments_and_memorials": "Памятники и мемориалы",
"historic": "Исторический",
"other_buildings_and_structures": "Другие здания и сооружения",
"interesting_places": "Интересные места",
"historic_architecture": "Историческая архитектура",
"architecture": "Архитектура",
"children_museums":"Детские музеи",
"puppetries":"кукольные представления",
"bridges":"Мосты",
"other_bridges":"Мосты",
"accomodations":"Жильё",
"other_hotels":"Отели",
"other":"Другое",
"unclassified_objects":"Другое",
"historic_object":"Исторический объект",
"circuses": "Цирки",
"zoos": "Зоопарки",
"fashion_museums": "Музеи моды",
"archaeological_museums": "Археологические музеи",
"destroyed_objects": "Уничтоженные объекты",
"historic_settlements": "Исторические поселения",
"fountains": "Фонтаны",
"installation": "Инсталляции",
"tourist_object": "Туристический объект",
"open_air_museums": "Музеи под открытым небом",
"other_nature_conservation_areas": "Другие природоохраннные территории",
"castles": "Замки",
"cemeteries": "Кладбища",
"planetariums": "Планетарии",
"triumphal_archs": "Триумфальные арки",
"defensive_walls": "Оборонительные стены",
"catholic_churches": "Католические церкви",
"water_towers": "Водонапорные башни",
"historic_house_museums": "Музеи исторических домов",
"other_archaeological_sites": "Другие археологические памятники",
"archaeology": "Археология",
"military_museums": "Военные музеи",
"children_theatres": "Детские театры"
}
cities = ['EKB', 'NN', 'Vladimir', 'Yaroslavl']
data_path = "/home/user/Загрузки/"
ctg = []
# for city in cities:
#     df = pd.read_csv(data_path + city + "_places.csv")
#     df = df.dropna(subset='Name')
#     df['Name'] = df['Name'].drop_duplicates()
#     if city == "Yaroslavl":
#         city = "yaroslavl"
#         df['image'] = pd.read_csv(data_path + city + "_images.csv")['img']
#     else:
#         df['image'] = pd.read_csv(data_path + city + "_images.csv")['image']
#     for i in range(len(df)):
#         Image.objects.create(name=f"{df.iloc[i]['Name']}", image=f'{df.iloc[i]["image"]}')
#
#     # df = pd.read_csv("server/NN_places.csv")
#     #
#     for i in range(len(df)):
#         place = Places.objects.create(my_id=i, XID=f"{df.iloc[i]['XID']}", name=f"{df.iloc[i]['Name']}",
#                                       city=f"{df.iloc[i]['City']}", OSM=f"{df.iloc[i]['OSM']}",
#                                       Lon=f"{df.iloc[i]['Lon']}", Lat=f"{df.iloc[i]['Lat']}")
#         place.save()
#         for j in df.iloc[i]['Kind'].split(','):
#             if j not in ctg:
#                 ctg.append(j)
#                 c = Category.objects.create(name=ctg_dict.get(j, j))
#                 c.save()
#                 place.category.add(c)
#             else:
#                 c = Category.objects.filter(name=ctg_dict.get(j, j))[0]
#                 place.category.add(c)
#
# df = pd.read_csv("server/NN_images.csv")

