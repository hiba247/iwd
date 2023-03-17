from django.urls import path
from core import views

urlpatterns = [
    path('posts/', views.PostsList.as_view()),
    path('users/', views.UsersList.as_view()),
    path('last_login/', views.ConsumptionCheck.as_view()),
   # path('articles/', scrapper.scrapper()),
    path('create_post/', views.CreatePost.as_view()),  
    path('complete_info/', views.CompleteInfo.as_view()),
    path('events/', views.GetEvents.as_view()),
    path('events/<slug:slug>', views.GetEvent.as_view())
    path('events/<slug:slug>/reserver', views.Reserver.as_view()),

]
