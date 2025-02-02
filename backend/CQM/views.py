from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("This is the index page.")
    return render(request, "index.html")

# Create your views here.
