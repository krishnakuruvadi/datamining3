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
    api_key = settings.GOOGLE_API
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
            try:
                r = UserRatings.objects.get(attraction=popular, user=uobj)
            except UserRatings.DoesNotExist:
                c += 1
                context['user_recommendations'].append(attraction_to_dict(ure.attraction))
                if c > 5:
                    break
        zip_codes = list()
        for i in zip_code.split(","):
            j = i.replace(' ','')
            zip_codes.append(j)
        zip_objs = ZipCode.objects.filter(country=country, zip_code__in=zip_codes)
        c = 0
        for popular in Attraction.objects.filter(zip_code__in=zip_objs).order_by('-number_of_ratings','-rating'):
            try:
                r = UserRatings.objects.get(attraction=popular, user=uobj)
            except UserRatings.DoesNotExist:
                c += 1
                context['popular_ratings'].append(attraction_to_dict(popular))
                if c > 5:
                    break
        
    print("context", context)
    
    return render(request, "home.html", context)


def add_user_rating(request, attraction_id, user_id):
    context = dict()
    print(f'attraction_id {attraction_id} user_id {user_id}')
    context['curr_module_id'] = 'id_dashboard_module'
    context['user_id'] = user_id
    context['attraction_id'] = attraction_id
    a = Attraction.objects.get(id=attraction_id)
    u = User.objects.get(username=user_id)
    context['attraction_name'] = a.name
    context['user_name'] = u.last_name+", "+u.first_name
    r = None
    try:
        r = UserRatings.objects.get(attraction = a, user=u)
        context['rating'] = r.rating
    except Exception as ex:
        pass
    if request.method == 'POST':
        print(request.POST)
        #user = request.POST['user']
        #attraction = request.POST['attraction']
        context['rating'] = request.POST['rating']
        try:
            if r:
                r.rating = request.POST['rating']
                r.save()
                context['message_color'] = 'green'
                context['message'] = 'Updated rating successfully'
            else:
                UserRatings.objects.create(attraction = a,
                rating = request.POST['rating'],
                user=u)
                context['message_color'] = 'green'
                context['message'] = 'Added rating successfully'
        except Exception as ex:
            print(f'failed to add user rating {ex}')
            context['message_color'] = 'red'
            context['message'] = 'Failed to add rating'
    
    print("context", context)
    
    return render(request, "add_user_rating.html", context)