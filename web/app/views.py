# Create your views here.

from django.http import HttpResponse

def default(request):
    return HttpResponse("Whoop")