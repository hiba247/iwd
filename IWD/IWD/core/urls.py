from django.urls import path
from core import views

urlpatterns = [
    path('users/', views.UsersList.as_view()),
    path('users/<int:id>/', views.UserDetails.as_view()),
    path('last_login/', views.StreakCheck.as_view()),
    path('complete_info/', views.CompleteInfo.as_view()),
    path('streak_update/', views.StreakUpdate.as_view())
]

urlpatterns += [
    path('posts/', views.PostsList.as_view()),
    path('create_post/', views.CreatePost.as_view()),
    path('posts/<int:id>/', views.PostDetails.as_view()),
    path('post/<int:id>/upvote/', views.Upvote.as_view()),
]

urlpatterns += [
    path('events/', views.GetEvents.as_view()),
    path('events/<slug:slug>/reserver/', views.Reserver.as_view()),
]

urlpatterns += [
    path('psychologist_register/', views.PsychologistRegister.as_view()),
    path('psychologists/', views.PsychologistList.as_view()),
    path('add_task/', views.AddTask.as_view())
]

urlpatterns += [
    path('articles/', views.ArticlesView.as_view()),
    path('add_article/', views.AddArticle.as_view()),
    path('add_event/',views.AddEvent.as_view()),
]

urlpatterns += [
    path('start_premium/', views.BecomePremium.as_view()),
    path('submit_task/', views.SubmitTask.as_view()),
    path('my_tasks/', views.TasksList.as_view())
]