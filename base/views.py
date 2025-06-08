from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create from django.http import HttpResponse

# rooms=[{'id':1,'name':"learning python"},
#        {'id':2,'name':"let's design"},
#        {'id':3,'name':"web developement"}
       
#        ]
def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |Q(name__icontains=q)|Q(description__icontains=q))
    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context);
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('created')
    if(request.method=="POST"):
        message=Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room
        )
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages}
    return render(request,'base/room.html',context)
@login_required(login_url='login')
def CreateRoom(request):
    form=RoomForm()
    if(request.method=='POST'):
        form=RoomForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if(room.host!=request.user):
        return HttpResponse("you're not allowed here my friend ")
    if(request.method=='POST'):
        form=RoomForm(request.POST,instance=room)
        if(form.is_valid()):
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def DeleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if(room.host!=request.user):
        return HttpResponse("you're not allowed here my friend ")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})



def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user does not exists")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)  
            return redirect('home')
        else:
            messages.error(request,"password is false ..try again")
    
    context={'page':page}
    return render(request,"base/login_register.html",context)
def Logout(request):
    logout(request)
    return redirect('home')
def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"an error occured during registration")
    context={'form':form}
    return render(request,'base/login_register.html',context)
