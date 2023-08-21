from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserRatings, UserRecommendations

from internals.models import Attraction, ZipCode
from django.conf import settings


# Create your views here.

def attraction_to_dict(attraction):
    api_key = settings.GOOGLE_API
    types = list()
    if attraction.is_park:
        types.append('Park')
    if attraction.is_tourist_attraction:
        types.append('Tourist Attraction')  
    if attraction.is_point_of_interest:
        types.append('Point of Interest')
    if attraction.is_establishment:
        types.append('Establishment')
    photo_link = "https://www.weddingsbylomastravel.com/images/paquetes/default.jpg"
    if attraction.photo_reference != "":
        photo_link = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={attraction.photo_reference}&key={api_key}"
            
    return {
                'name': attraction.name,
                'id':attraction.id,
                'types': ", ".join(types),
                'photo_url': photo_link,
                'place_id':attraction.place_id,
                'rating':attraction.rating,
                'number_of_ratings':attraction.number_of_ratings
            }

def user_rating_to_dict(user_rating):
    attraction = user_rating.attraction
    types = list()
    if attraction.is_park:
        types.append('Park')
    if attraction.is_tourist_attraction:
        types.append('Tourist Attraction')  
    if attraction.is_point_of_interest:
        types.append('Point of Interest')
    if attraction.is_establishment:
        types.append('Establishment')
    photo_link = "https://www.weddingsbylomastravel.com/images/paquetes/default.jpg"
    if attraction.photo_reference != "":
        photo_link = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={attraction.photo_reference}&key={api_key}"
            
    return {
                'name': attraction.name,
                'id':attraction.id,
                'types': ", ".join(types),
                'photo_url': photo_link,
                'place_id':attraction.place_id,
                'rating':attraction.rating,
                'number_of_ratings':attraction.number_of_ratings,
                'your_rating':user_rating.rating,
            }

def home_view(request, *args, **kwargs):
    context = dict()
    context['curr_module_id'] = 'id_dashboard_module'
    context['countries'] = ["India", "USA"]
    context['users'] = list()

    for uobj in User.objects.all():
        context['users'].append(uobj.username)

    if request.method == 'POST':
        print(request.POST)
        user = request.POST['user']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        context['user'] = user
        context['country'] = country
        context['zip_code'] = zip_code

        context['user_ratings'] = list()
        context['user_recommendations'] = list()
        context['popular_ratings'] = list()
        uobj = User.objects.get(username=user)
        c = 0
        for uro in UserRatings.objects.filter(user=uobj):
            c += 1
            context['user_ratings'].append(user_rating_to_dict(uro))
            if c > 5:
                break
        c = 0
        for ure in UserRecommendations.objects.filter(user=uobj):
            c += 1
            context['user_recommendations'].append(attraction_to_dict(ure.attraction))
            if c > 5:
                break
        zip_obj = ZipCode.objects.get(country=country, zip_code=zip_code)
        c = 0
        for popular in Attraction.objects.filter(zip_code=zip_obj).order_by('-number_of_ratings','-rating'):
            c += 1
            context['popular_ratings'].append(attraction_to_dict(popular))
            if c > 5:
                break
        
    print("context", context)
    
    return render(request, "home.html", context)