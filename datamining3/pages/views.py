from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.



def home_view(request, *args, **kwargs):
    context = dict()
    context['curr_module_id'] = 'id_dashboard_module'
    context['countries'] = ["India", "USA"]
    context['users'] = list()
    for user in User.objects.all():
        context['users'].append(user.username)

    if request.method == 'POST':
        print(request.POST)
        user = request.POST['user']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        context['user'] = user
        context['country'] = country
        context['zip_code'] = zip_code
        
    print("context", context)
    
    return render(request, "home.html", context)