# Create your views here.
from django.shortcuts import render

def participants(request):
    return render(request, 'participants.html')