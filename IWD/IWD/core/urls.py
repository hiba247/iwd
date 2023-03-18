from django.urls import path
from core import views

urlpatterns = [                                            
    path('users/', views.UsersList.as_view()),             # returns all users  
    path('users/<int:id>/', views.UserDetails.as_view()),  # returns details about a specific user
    path('last_login/', views.StreakCheck.as_view()),      # returns last time a specific user has logged in
    path('complete_info/', views.CompleteInfo.as_view()),  # used to complete a newly registered user's informations - only the email and age are required in the registration-
    path('streak_update/', views.StreakUpdate.as_view())   # used to update the streak of a specific user
]

urlpatterns += [
    path('posts/', views.PostsList.as_view()),             # returns all posts
    path('create_post/', views.CreatePost.as_view()),      # used to create a post
    path('posts/<int:id>/', views.PostDetails.as_view()),  # returns details about a specific post
    path('post/<int:id>/upvote/', views.Upvote.as_view()), # used by a user to upvote or undo an upvote of a post
    path('post/<int:id>/add_comment/', views.AddComment.as_view())    # user by a user to add a comment 
]

urlpatterns += [
    path('events/', views.GetEvents.as_view()),                     # returns all events
    path('events/<int:id>', views.EventDetails.as_view()),         # returns details about a specific event
    path('events/<slug:slug>/reserver/', views.Reserver.as_view()), # used by a user to make a reservation at an event
]

urlpatterns += [
    path('psychologist/register/', views.PsychologistRegister.as_view()),  # used by psychologists to register to the website
    path('psychologists/', views.PsychologistList.as_view()),              # returns all psychologists
    path('psychologist/login/', views.PsychologistLogin.as_view()),        # used by psychologists to login to the website
    path('add_task/', views.AddTask.as_view())                             # used by a psychologist to affect tasks to a specific patient of his
]

urlpatterns += [
    path('articles/', views.ArticlesView.as_view()),    # returns all articles
    path('add_article/', views.AddArticle.as_view()),   # used by an admin to add an article either by scrapping or manually
    path('add_event/',views.AddEvent.as_view()),        # used by an admin to add an event
]

urlpatterns += [
    path('start_premium/', views.BecomePremium.as_view()),   # used by a user to upgrade his account to premium -myProgress-
    path('submit_task/', views.SubmitTask.as_view()),        # used by a premium user to submit the tasks given to him by his psychologist
    path('my_tasks/', views.TasksList.as_view())             # returns all tasks of the signed in, premium user
]
