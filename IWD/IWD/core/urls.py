from django.urls import path
from core import views, scrapper

urlpatterns = [
    path('posts/', views.PostsList.as_view()),
    path('users/', views.UsersList.as_view()),
    path('last_login/', views.ConsumptionCheck.as_view()),
    path('articles/', scrapper.scrapper()),
    path('createpost/', views.CreatePost.as_view())
]
