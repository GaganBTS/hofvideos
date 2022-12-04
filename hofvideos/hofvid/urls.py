from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('dashboard',dashboard,name='dashboard'),
    path('signup',Signup.as_view(),name='signup'),
    path('login',auth_views.LoginView.as_view(),name='login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    path('halloffame/createhall',CreateHall.as_view(),name='create_hall'),
    path('halloffame/<int:pk>',DetailHall.as_view(),name='detail_hall'),
    path('halloffame/<int:pk>/update',UpdateHall.as_view(),name='update_hall'),
    path('halloffame/<int:pk>/delete',DeleteHall.as_view(),name='delete_hall'),
    path('halloffame/<int:pk>/addvideo',add_video, name='add_video'),
    path('video/search',search_video, name='video_search'),
    path('video/<int:pk>/delete',DeleteVideo.as_view(),name='delete_video')

]
