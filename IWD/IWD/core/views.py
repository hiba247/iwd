from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import *
from rest_framework import permissions
from rest_framework import status,generics
from rest_framework.response import Response
from django.contrib.auth import login, logout, get_user_model
from .serializers import *
from django.middleware.csrf import get_token
from django.core.paginator import Paginator


User = get_user_model()

def sendResponse(data, message):
    res = {
        'success': True,
        'data': data,
        'message': message
    }
    return JsonResponse(res, safe=False)

def sendErrorMessage(message):
    res = {
        'success': False,
        'message': message
    }
    return JsonResponse(res, safe=False)

# ------------------------- auth views --------------------------- #


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
        

class LoginView(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(get_token(request))
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
        #return Response(None, status=status.HTTP_202_ACCEPTED)


class ProfileView(generics.RetrieveAPIView):
    
    serializer_class = UserSerializer

    def get_object(self):
        return sendResponse(self.request.user, 'User data')
        #return self.request.user


class LogoutView(APIView):
    
    def post(self, request, format=None):
        logout(request)
        return sendResponse(None, 'User logged out')
        #return Response(None, status=status.HTTP_204_NO_CONTENT)
#-------------------------------------------------------------------------#

# --------------------------- Post views ---------------------------------#

class PostsList(APIView):
    """
    get all posts
    """
    def get(self, request, format=None):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return sendResponse(serializer.data, 'All posts')
        except Exception as e:
            return sendErrorMessage(str(e))
        
class CreatePost(APIView):
   def post(self,request,format=None):
    context= request.POST  
    title=context.get("title")
    content=context.get("content")
    print(request.user)
    user=request.user 
    #user=User.objects.get(id=userid)
    post =Post.objects.create(title=title,content=content,user=user)

    serilizer = PostSerializer(post)
    print(serilizer)
    return sendResponse(serilizer.data,'the post')

# -------------------------------------------------------------------------#

# ------------------------- User views ----------------------------------- #
class UsersList(APIView):
    """
    get all users
    """
    def get(self, request, format=None):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return sendResponse(serializer.data, 'all users')
        except Exception as e:
            return sendErrorMessage(str(e))
        
class CompleteInfo(APIView):
    def post(self,request,format=None):
        print(request)
        context= request.POST  
        first_name=context.get("first_name")
        last_name=context.get("last_name")
        gender=context.get("gender") 
        usr=request.user 
        addiction=context.get("addiction")
        print(usr)
        User.objects.filter(id=usr.id).update(first_name=first_name,last_name=last_name,gender=gender,addiction=addiction)
        serilizer = UserSerializer(usr)
        return sendResponse(serilizer.data,'the post')
        
#-------------------------------------------------------------------------#

# ----------------------- Consumption check function ---------------------#

class ConsumptionCheck(APIView):
    def get(self, request, format=None):
        try:
            current_user = request.user
            serializer = UserSerializer(current_user)
            last_login = serializer.data['last_login']
            return sendResponse(last_login, 'last login of current user')
        except Exception as e:
            return sendErrorMessage(str(e))
            

# ------------------- Events views --------------------------#
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
       
  
class getevents(APIView):
       def get(self, request, format=None):
        try:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return sendResponse(serializer.data, 'all events')
        except Exception as e:
            return sendErrorMessage(str(e))      

class Reserver(APIView):
    def post(self,request,slug,format=None):
        event=Event.objects.get(pk=slug)
        user=request.user
        event.num_places=event.num_places-1
        event.save()
        event.users.add(user)
        serializer = EventSerializer(event, many=True)
        return sendResponse(serializer.data,'place reservé')

class Comments(APIView):
    def get(self, request, format=None):
        try:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return sendResponse(serializer.data, 'all comments')
        except Exception as e:
            return sendErrorMessage(str(e))      

class AddComment(APIView):
    def post(self, request, slug,format=None):
        try:
            content = request.POST.get('content')
            post=Post.objects.get(pk=slug)

            user=request.user
            new_comment = Comment(content=content, user=user,post=post)
            new_comment.save()
            serializer = CommentSerializer(new_comment)
            return sendResponse(serializer.data, 'New event added')
        except Exception as e:
            return sendErrorMessage(str(e))
