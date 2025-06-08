from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room_updated/',views.CreateRoom,name='create-room'),
    path('Update-room/<str:pk>/',views.UpdateRoom,name='Update-room'),
    path('Delete-room/<str:pk>/',views.DeleteRoom,name='Delete-room'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='deleteMessage'),
    path('userProfile/<str:pk>/',views.userProfile,name='userprofile')

]