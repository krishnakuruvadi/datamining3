from django.shortcuts import render

# Create your views here.



def home_view(request, *args, **kwargs):
    context = dict()
    context['curr_module_id'] = 'id_dashboard_module'
    print("context", context)
    return render(request, "home.html", context)