from django.shortcuts import render ,redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login ,logout
from .models import Room , Topic , Message ,User
from .forms import RoomForm ,UserForm  ,MyUserCreationForm
# Create your views here.

# rooms = [
#     {'id':1 ,'name':"Lets Learn Python"},
#     {'id':2 ,'name':"Design With ME"},
#     {'id':3 ,'name':"Frontend Developers"}
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password') 

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request ,'User does not exist')

        user = authenticate(request ,email=email ,password=password)
        if user is not None:
            login(request ,user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password Does not exist' )


    context = {'page':page}
    return render(request ,'basee/login_register.html' ,context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #form is not sent what if theres a error
            user.username = user.username.lower() # making sure that entered text is in Lower case
            user.save()
            login(request ,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request ,'basee/login_register.html' ,{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) | # icontains is case insensitive 
        Q(name__icontains=q) |          # contains is case sensitive which is Lower /Capital
        Q(description__icontains=q) 
        )

    topics = Topic.objects.all().order_by('name')[0:5] # topics ordered alphabetically and limited by 6 
    room_count = rooms.count()
    room_messages  = Message.objects.filter( Q(room__topic__name__icontains=q))



    context = {'rooms':rooms ,'topics':topics ,'room_count':room_count ,'room_messages':room_messages}
    return render(request ,'basee/home.html', context)

def room(request ,pk):
    room = Room.objects.get(id = pk)
    room_messages =room.message_set.all() #to get all atrib/method of child class
    participants = room.participants.all()
    room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    context = {'room':room ,'room_messages': room_messages ,'participants' : participants}
    return render(request ,'basee/room.html',context)  

def userProfile(request ,pk):
    user = User.objects.get(id=pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context = {'user':user ,'rooms':rooms ,'room_messages':room_messages ,'topics':topics}
    return render(request ,'basee/profile.html' ,context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic') # get value if not exist creates it  
        topic, created = Topic.objects.get_or_create(name = topic_name) 
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
        return redirect('home') 
    
    context = {'form': form , 'topics': topics}
    return render(request, 'basee/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request ,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host :
        return HttpResponse('You Are Not Allowed To Do That ! ')

    if request.method == 'POST':
        topic_name = request.POST.get('topic') # get value if not exist creates it  
        topic, created = Topic.objects.get_or_create(name = topic_name) 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form ,'topics':topics , 'room':room}
    return render(request ,'basee/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request ,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host :
        return HttpResponse('You Are Not Allowed To Do That ! ')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request ,'basee/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request ,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user :
        return HttpResponse('You Are Not Allowed To Do That ! ')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request ,'basee/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST': # .FILES sends files
        form = UserForm(request.POST ,request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile' ,pk = user.id)
    
    
    context = {'form':form}
    return render(request ,'basee/update_user.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q).order_by('name')
    context = {'topics': topics}
    return render(request ,'basee/topics.html', context) 

def activityPage(request):

    room_messages = Message.objects.all()
    context = {'room_messages':room_messages }
    return render(request ,'basee/activity.html', context)