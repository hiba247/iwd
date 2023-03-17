from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Post, User
from .serializers import *

# Create your views here.

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
    """"
    create new post
    """
    pass
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
        
#-------------------------------------------------------------------------#