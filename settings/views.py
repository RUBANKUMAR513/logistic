from django.http import HttpResponse

def index(request):
    return HttpResponse("Settings Home Page")

def settings_list(request):
    return HttpResponse("List of Settings")