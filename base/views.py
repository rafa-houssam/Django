from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
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
    topics=Topic.objects.all()[0:5]
    room_messages=Message.objects.all().order_by('-created').filter(Q(room__topic__name__icontains=q))[0:5]
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context);
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room
        )

        # ✅ Add the user to the participants
        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def CreateRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if(request.method=='POST'):
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if(room.host!=request.user):
        return HttpResponse("you're not allowed here my friend ")
    if(request.method=='POST'):
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
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
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
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

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if(message.user!=request.user):
        return HttpResponse("you're not allowed here my friend ")
    if request.method=='POST':
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':message})

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()

    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)  # <-- FIX: include instance
        if form.is_valid():
            form.save()  # no need to assign to user again
            return redirect('userprofile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else '' 
    topics=Topic.objects.all().filter(Q(name__icontains=q))
    context={'topics':topics}
    return render(request,'base/topics.html',context)
def activityPage(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    room_messages=Message.objects.all().order_by('-created').filter(Q(room__topic__name__icontains=q))
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)