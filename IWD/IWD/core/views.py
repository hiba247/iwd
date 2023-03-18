from django.http import JsonResponse
from rest_framework.views import APIView
from .models import *
from rest_framework import permissions
from django.contrib.auth import login, logout, get_user_model
from .serializers import *
from django.middleware.csrf import get_token

User = get_user_model()


# ---------------------------- Base functions --------------------------- #
"""
A function used to return data in JSON format with a success boolean and an additional message, used for successful requests
"""
def sendResponse(data, message):
    res = {
        'success': True,
        'data': data,
        'message': message
    }
    return JsonResponse(res, safe=False)

"""
A function used to return a JSON response with a success boolean and a message, used for unsuccessful requests
"""
def sendErrorMessage(message):
    res = {
        'success': False,
        'message': message
    }
    return JsonResponse(res, safe=False)
#----------------------------------------------------------------------#




# --------------------------------- Auth views ------------------------------------- #
"""
A class-based view used to register users to the website based on email, age and password fields
"""
class RegisterView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            age = int(request.POST.get('age'))
            
            if (not email) or (not password):
                return sendErrorMessage('Email and password are required')
            if(age<21):
                return sendErrorMessage('You do not meet the age requirements')
            if(User.objects.filter(email=email).exists()):
                return sendErrorMessage('User already exists with given email')
            
            user = User(email=email, password=password, age=age, premium=False,
                                            streak=0)
            user.save()
            serializer = UserSerializer(user)
            return sendResponse(serializer.data, 'User registered')
        except Exception as e:
            return sendErrorMessage(str(e))
        

"""
A class-based view used by users to login to the website based on email and password fields
the login is used by setting a user-specific session variable with the built-in login() function
"""
class LoginView(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if user:
            serializer = UserSerializer(user)
            if(serializer.data['password'] == password):
                login(request, user)
            else:
                return sendErrorMessage('Wrong password')
        else:
            return sendErrorMessage('No user found for given email')
        return sendResponse(get_token(request), 'User logged in, fetched CSRF Token')


"""
A class-based view used to logout users from the website
It uses the logout() built-in function to unset the session variable
"""
class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return sendResponse(None, 'User logged out')
#----------------------------------------------------------------------------------#




# ------------------------------------ Post views ------------------------------------#

"""
A class-based view used to get all posts
"""
class PostsList(APIView):
    def get(self, request, format=None):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return sendResponse(serializer.data, 'All posts')
        except Exception as e:
            return sendErrorMessage(str(e))


"""
A class-based view used to get the details of a specific post
"""
class PostDetails(APIView):
    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(pk=id)
            serializer = PostSerializer(post)
            return sendResponse(serializer.data, f'Post #{post.id}')
        except Exception as e:
            return sendErrorMessage(str(e))
         
            
"""
A class-based view used to create a post
"""
class CreatePost(APIView):
   def post(self,request,format=None):
    context= request.POST  
    title=context.get("title")
    content=context.get("content")
    photo=request.FILES.get('photo')
    user=request.user 
    #user=User.objects.get(id=userid)
    post =Post.objects.create(title=title,content=content,user=user, photo=photo)

    serilizer = PostSerializer(post)
    return sendResponse(serilizer.data,'the post')

# ---------------------------------------------------------------------------------------#






# ------------------------- User views ----------------------------------- #

"""
A class-based view used to get all users
"""
class UsersList(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return sendResponse(serializer.data, 'all users')
        except Exception as e:
            return sendErrorMessage(str(e))
        
"""
A class-based view used to get all the details of a specific user
"""
class UserDetails(APIView):
    def get(self, request, id, format=None):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            return sendResponse(serializer.data, f'User {user.id}')
        except Exception as e:
            return sendErrorMessage(str(e))
    
"""
A class-based view used by users to complete entering their data after the registration
"""
class CompleteInfo(APIView):
    def post(self,request,format=None):
        context= request.POST  
        first_name=context.get("first_name")
        last_name=context.get("last_name")
        gender=context.get("gender") 
        usr=request.user
        addiction=context.get("addiction")
        photo = request.FILES.get('photo')
        User.objects.filter(id=usr.id).update(first_name=first_name,last_name=last_name,gender=gender,addiction=addiction, photo=photo)
        serilizer = UserSerializer(usr)
        return sendResponse(serilizer.data,f'Updated user #{usr.id} info')
        
#-------------------------------------------------------------------------#





# ------------------------- Consumption check function -------------------------#

"""
A class-based view used to get the last time the current user logged in
This view is used as a tool for the following one
"""
class StreakCheck(APIView):
    def get(self, request, format=None):
        try:
            current_user = request.user
            serializer = UserSerializer(current_user)
            last_login = serializer.data['last_login']
            return sendResponse(last_login, 'last login of current user')
        except Exception as e:
            return sendErrorMessage(str(e))

"""
A class-based view used to update the streak attribute of the user (either increment it or reset it to 0)
"""        
class StreakUpdate(APIView):
    def post(self, request, format=None):
        try:
            user = request.user
            boolean = int(request.POST.get('response'))
            if(boolean == 1):
                user.streak += 1
            else:
                user.streak = 0
            user.save()
            serializer = UserSerializer(user)
            return sendResponse(serializer.data, 'streak updated')
        except Exception as e:
            return sendErrorMessage(str(e))
            
# ----------------------------------------------------------------------#






# ------------------------------ Events views ---------------------------------#

"""
A class-based view used by the admin to add an event
"""
class AddEvent(APIView):
    def post(self, request, format=None):
        try:
            price = request.POST.get('price')
            place = request.POST.get('place')
            date=request.POST.get('date')
            num_places = int(request.POST.get('num_places'))
            new_event = Event(price=price, place=place, num_places=num_places,date=date)
            new_event.save()
            serializer = EventSerializer(new_event)
            return sendResponse(serializer.data, 'New event added')
        except Exception as e:
            return sendErrorMessage(str(e))
       
"""
A class-based view used to get all the events
"""
class GetEvents(APIView):
       def get(self, request, format=None):
        try:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return sendResponse(serializer.data, 'All events')
        except Exception as e:
            return sendErrorMessage(str(e))      

"""
A class-based view used to get details of a specific event
"""
class EventDetails(APIView):
    def get(self, request, id, format=None):
        try:
            event = Event.objects.get(pk=id)
            serializer = EventSerializer(event)
            return sendResponse(serializer.data, f'Event {event.description}')
        except Exception as e:
            return sendErrorMessage(str(e))
    
"""
A class-based view used by the user to make a reservation for an event
"""   
class Reserver(APIView):
    def post(self,request,slug,format=None):
        event=Event.objects.get(pk=slug)
        user=request.user
        event.num_places=event.num_places-1
        event.save()
        event.users.add(user)
        serializer = EventSerializer(event, many=True)
        return sendResponse(serializer.data,'place reservé')
# ---------------------------------------------------------------------- #






# ----------------------- Comments views -------------------- #

"""
A class-based view used to retrieve all comments
"""
class Comments(APIView):
    def get(self, request, format=None):
        try:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return sendResponse(serializer.data, 'all comments')
        except Exception as e:
            return sendErrorMessage(str(e))      

"""
A class-based view used by a user to add a comment
"""
class AddComment(APIView):
    def post(self, request, id,format=None):
        try:
            content = request.POST.get('content')
            post=Post.objects.get(pk=id)

            user=request.user
            new_comment = Comment(content=content, user=user,post=post)
            new_comment.save()
            serializer = CommentSerializer(new_comment)
            return sendResponse(serializer.data, 'New comment added')
        except Exception as e:
            return sendErrorMessage(str(e))
# ------------------------------------------------------------------------- #





        
# ---------------------------- Upvotes views ---------------------------- #

"""
A class-based view used by a user to upvote (or remove an upvote to) a post
"""
class Upvote(APIView):
    def post(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            user = request.user
            serializer = PostSerializer(post)
            print(serializer.data)
            if(user.id in serializer.data['upvoters']):
                post.upvote_count -= 1
                post.upvoters.remove(user)
                return sendResponse(serializer.data, 'Post unliked')
            post.upvote_count += 1
            post.save()
            post.upvoters.add(user)
            return sendResponse(serializer.data, 'Post liked')
        except Exception as e:
            return sendErrorMessage(str(e))
# ----------------------------------------------------------------------- #        
        
        
        
        

# ---------------------------- Psychologist views ------------------------------ #

"""
A class-based view used to register a new psychologist to the website
"""
class PsychologistRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            if (not email) or (not password):
                return sendErrorMessage('Email and password are required')
            if(not first_name) or (not last_name):
                return sendErrorMessage('Please enter your first and last names')
            if(User.objects.filter(email=email).exists()):
                return sendErrorMessage('Psychologist already exists with given email')
            
            user = Psychologist(email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            serializer = PsychologistSerializer(user)
            return sendResponse(serializer.data, 'Psychologist registered')
        except Exception as e:
            return sendErrorMessage(str(e))
        
"""
A class-based view used to login a psychologist to the website
"""
class PsychologistLogin(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        psychologist = Psychologist.objects.get(email=email)
        if user:
            serializer = PsychologistSerializer(psychologist)
            if(serializer.data['password'] == password):
                login(request, psychologist)
            else:
                return sendErrorMessage('Wrong password')
        else:
            return sendErrorMessage('No user found for given email')
        return sendResponse(get_token(request), 'User logged in, fetched CSRF Token')
    
"""
A class-based view used to retrieve all psychologists
"""
class PsychologistList(APIView):
    def get(self, request):
        try:
            psychologists = Psychologist.objects.all()
            serializer = PsychologistSerializer(psychologists, many=True)
            return sendResponse(serializer.data, 'All psychologists')
        except Exception as e:
            return sendErrorMessage(str(e))
# ------------------------------------------------------------------------- #        
        
        
        
        
        
# ---------------------------- myProgress views ------------------------ #

"""
A class-based view used by the user to upgrade his account to premium (boolean premium = True)
"""
class BecomePremium(APIView):
    def post(self, request, format=None):
        try:
            cause = request.POST.get('cause_of_addiction')
            frequency = request.POST.get('frequency_of_use')
            psychologist = Psychologist.objects.get(pk=int(request.POST.get('psychologist_id')))
            user = request.user
            user.cause_of_addiction = cause
            user.frequency_of_use = frequency
            user.assigned_psychologist = psychologist
            user.premium = True
            user.save()
            serializer = UserSerializer(user)
            return sendResponse(serializer.data, 'User upgraded to premium')
        except Exception as e:
            return sendErrorMessage(str(e))
        
"""
A class-based view used to retrieve all tasks of a specific user
""" 
class TasksList(APIView):
    def get(self, request):
        try:
            user = request.user
            tasks = Task.objects.filter(user=user)
            serializer = TaskSerializer(tasks, many=True)
            return sendResponse(serializer.data , f'Tasks of User #{user.id}')
        except Exception as e:
            return sendErrorMessage(str(e))
    

"""
A class-based view used by a premium user to submit his done tasks that were assigned to him by his psychologist
and calculating the progress based on the goal of the task
"""
class SubmitTask(APIView):
    def post(self, request, format=None):
        try:
            task = Task.objects.get(pk = int(request.POST.get('task_id')))
            if(task.progress == 1):
                serializer = TaskSerializer(task)
                return sendResponse(serializer.data, 'Task completed, congratulations')
            progress_value = task.progress + ( 1 / task.goal )
            task.progress = round(progress_value, 2)
            task.save()
            serializer = TaskSerializer(task)
            if(task.progress == 1):
                serializer = TaskSerializer(task)
                return sendResponse(serializer.data, 'Task completed, congratulations')
            return sendResponse(serializer.data, 'Progress updated')
        except Exception as e:
            return sendErrorMessage(str(e))
    
# -------------------------------------------------------------------#        
        
        
        
        
        
# --------------------------- Admin views -------------------------- #

"""
A class-based view used to retrieve all articles
"""
class ArticlesView(APIView):
    def get(self, request):
        try:
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return sendResponse(serializer.data, 'All articles')
        except Exception as e:
            return sendErrorMessage(str(e))
        

"""
A class-based view used by the admin to add an article
"""
class AddArticle(APIView):
    def post(self, request):
        try:
            option = request.POST.get('option')
            if(option==1):
                admin = request.user
                title = request.POST.get('title')
                content = request.POST.get('content')
                added_by = admin        
                new_article = Article(title=title, content=content, added_by=added_by)
                serializer = ArticleSerializer(new_article)
                return sendResponse(serializer.data, 'Article added')
            elif(option==2):
                return sendErrorMessage('The scrapper is down currently, we apologize for this inconvenience')
        except Exception as e:
            return sendErrorMessage(str(e))
        
        
#--------------------------------------------------------------------#



#-------------------------- Psychologist views -----------------------#

"""
A class-based view used by a psychologist to add tasks to one of his patients
"""
class AddTask(APIView):
    def post(self, request):
        try:
            description = request.POST.get('description')
            goal = int(request.POST.get('goal'))
            user = User.objects.get(pk = int(request.POST.get('user_id')))
            new_task = Task(description=description, goal=goal, user=user)
            new_task.save()
            serializer = TaskSerializer(new_task)
            return sendResponse(serializer.data, f'Task added to user #{user.id}')
        except Exception as e:
            return sendErrorMessage(str(e))
        
