from django.shortcuts import render
from .models import Room

# Create from django.http import HttpResponse

# rooms=[{'id':1,'name':"learning python"},
#        {'id':2,'name':"let's design"},
#        {'id':3,'name':"web developement"}
       
#        ]
rooms=Room.objects.all()
def home(request):
    context={'rooms':rooms}
    return render(request,'base/home.html',context);
def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)
