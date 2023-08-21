from huey.contrib.djhuey import task, periodic_task, db_task, db_periodic_task, on_startup
from huey import crontab
from .models import Task, TaskState
import datetime
from internals.models import ZipCode
from django.conf import settings
import requests
from django.db import IntegrityError
from internals.helper import add_or_update_attractions



def set_task_state(name, state):
    try:
        task = Task.objects.get(task_name=name)
        
        if state.value == TaskState.Running.value:
            task.current_state = state.value
            task.last_run = datetime.datetime.now()
        else:
            task.last_run_status = state.value
            task.current_state = TaskState.Unknown.value
        task.save()
    except Task.DoesNotExist:
        print('Task ',name,' doesnt exist')


def add_zip_code(country, zip_code):
    api_key = settings.GOOGLE_API
    url = f'https://maps.googleapis.com/maps/api/geocode/json?key={api_key}&components=postal_code:{zip_code}'
    print(f'fetching coordinates for {zip_code} using url {url}')
    response = requests.get(url, timeout=10)
    data = response.json()

    print(f'data in add_zip_code {data}')
    if data['status'].lower() == 'ok':
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        print(f'found lat and long for {zip_code} {latitude} {longitude}')
        
        try:
            ZipCode.objects.create(country='USA', zip_code=zip_code, latitude=latitude, longitude=longitude)
            print(f'new zip code added {country} {zip_code} {latitude} {longitude}')
        except IntegrityError:
            print(f'zip code {zip_code} already being tracked')
    else:
        print(f"ignoring result {data} and status:{data['status']}")


@db_periodic_task(crontab(minute='0', hour='*/12'))
def get_local_attractions(radius = 10000 ):
    print('inside get_local_attractions')
    set_task_state('get_local_attractions', TaskState.Running)
    zip_code_objs = ZipCode.objects.all()

    if len(zip_code_objs) == 0:
        zip_codes = dict()
        zip_codes['USA'] = ['95123', '95035']
        for k,l in zip_codes.items():
            for zc in l:
                add_zip_code(k, zc)
        zip_code_objs = ZipCode.objects.all()

    for obj in zip_code_objs:
        print(f'fetching attractions for {obj.country} {obj.zip_code}')
        fetch_attractions(obj, radius)
    set_task_state('get_local_attractions', TaskState.Successful)



def fetch_attractions(zip_code_obj, radius):
    api_key = settings.GOOGLE_API
    keyword = "attraction" 
    location = zip_code_obj.latitude+","+zip_code_obj.longitude
     # Search radius in meters
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&location={location}&radius={radius}&keyword={keyword}"

    print(f'fetching attractions for {zip_code_obj.zip_code} using url {url}')
    response = requests.get(url, timeout=10)
    data = response.json()
    print(f'data in fetch_attractions {data}')
    if data['status'].lower() == 'ok':
        add_or_update_attractions(data['results'], zip_code_obj)
    else:
        print(f"ignoring result {data} and status:{data['status']}")