from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

def loginPage(request): # Don't use `login` for function name due to conflict.
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower() # Just consider lower case.
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request) # Deletes session ID token.
    return redirect('home')

def registerPage(request):
    page = 'register'

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() # Make sure it's lower case.
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter( # Rooms are shown at homepage center.
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all() # Topics are shown at homepage left side.
    rooms_messages = Message.objects.filter( # Messages are shown at homepage right side.
        Q(room__topic__name__icontains=q)
    )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
    'rooms_messages': rooms_messages
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room_message = Message.objects.create(
            body=request.POST.get('body'),
            room=room,
            user=request.user
            )
        room_message.save()

        room.participants.add(request.user)

        return redirect('room', pk=room.id) # Redirect is a must for a full page reload to avoid side effects.

    # Renamed to avoid conflict with imported messages.
    room_messages = room.message_set.all() # All the related tables.
    participants = room.participants.all()

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # Var name should be consistent with var name used by templates.
    rooms_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'rooms_messages': rooms_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login') # If session ID is not good, user cannot access this.
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login') # If session ID is not good, user cannot access this.
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not room owner")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context) 

@login_required(login_url='/login') # If session ID is not good, user cannot access this.
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not room owner")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='/login') # If session ID is not good, user cannot access this.
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not message writer")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='/login') # If session ID is not good, user cannot access this.
def updateUser(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)
    context = {'form': form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q) # If "q" is empty, this is equivalent of objects.all()
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)