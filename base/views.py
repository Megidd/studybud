from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id':1, 'name':'Let\'s learn Python.'},
    {'id':2, 'name':'Design with me.'},
    {'id':3, 'name':'Front-end developers.'},
]

def home(request):
    return render(request, 'home.html', {'rooms': rooms})

def room(request):
    return render(request, 'room.html')
