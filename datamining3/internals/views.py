from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)
from .models import ZipCode
from .helper import get_attractions
from django.conf import settings
import json
from django.contrib.auth.models import User
from tasks.tasks import add_zip_code

# Create your views here.
def common_list_view(request):
    context = dict()
    template = 'internals/common_list.html'
    context['curr_module_id'] = 'id_internals_module'
    return render(request, template, context)


def add_user(request):
    context = dict()
    template = 'internals/add_user.html'
    context['curr_module_id'] = 'id_internals_module'
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_id = request.POST['user_id']
        try:
            User.objects.create(
                username=user_id,
                first_name=first_name,
                last_name=last_name
            )
            context['message'] = 'Add user successful'
            context['message_color'] = 'green'
        except Exception as ex:
            context['message'] = 'Failed to add user'
            context['message_color'] = 'red'
            print(f'failed to add user {ex}')
    return render(request, template, context)


def add_zip_code_view(request):
    context = dict()
    template = 'internals/add_zip_code.html'
    context['curr_module_id'] = 'id_internals_module'
    context['countries'] = ['USA', 'India']
    if request.method == 'POST':
        print(request.POST)
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        try:
            add_zip_code(country=country, zip_code=zip_code)
            context['message'] = 'Add zip code successful'
            context['message_color'] = 'green'
        except Exception as ex:
            context['message'] = 'Failed to add zip code'
            context['message_color'] = 'red'
            print(f'failed to add zip code {ex}')
    return render(request, template, context)

class ZipCodeListView(ListView):
    template_name = 'internals/zip_code_list.html'
    model = ZipCode

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['curr_module_id'] = 'id_internals_module'
        return data

class UserListView(ListView):
    template_name = 'internals/user_list.html'
    model = User

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['curr_module_id'] = 'id_internals_module'
        return data

def attractions_list_view(request):
    api_key = settings.GOOGLE_API

    context = dict()
    template = 'internals/attraction_list.html'
    context['curr_module_id'] = 'id_internals_module'
    context['countries'] = ["India", "USA"]
    if request.method == 'POST':
        print(request.POST)
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        attractions = get_attractions(country, zip_code)
        context['attractions'] = list()
        context['zip_code'] = zip_code
        context['country'] = country
        for attraction in attractions:
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
            context['attractions'].append({
                'name': attraction.name,
                'id':attraction.id,
                'types': ", ".join(types),
                'photo_url': photo_link,
                'place_id':attraction.place_id,
                'rating':attraction.rating,
                'number_of_ratings':attraction.number_of_ratings
            })
    else:
        attractions = list()
    return render(request, template, context)