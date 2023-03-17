from django.urls import path
from core import views

urlpatterns = [
    path('posts/', views.PostsList.as_view()),
    path('users/', views.UsersList.as_view()),
    path('createpost/', views.CreatePost.as_view())
]
