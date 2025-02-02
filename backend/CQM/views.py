from django.shortcuts import render
from django.http import HttpResponse
from .models import fileUpload

def index(request):
    # return HttpResponse("This is the index page.")
    if request.method == "POST":
        fileSave = request.FILES.get("file")
        fileUpload.objects.create(file=fileSave)
    return render(request, "index.html")

# Create your views here.
