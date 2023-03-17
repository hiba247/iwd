from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Post
from rest_framework import permissions
from rest_framework import status,generics
from rest_framework.response import Response
from django.contrib.auth import login, logout, get_user_model
from .serializers import *
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
class RegisterView():
    pass

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutView(APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
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
