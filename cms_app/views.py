from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer, PostSerializer, LikeSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import post, Like

# user registration view
class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "Account is created."
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)
            
     
    
# user login view
class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)  # get jwt token from srializer.py
            
            return Response(response, status=status.HTTP_200_OK)
            
        
        except Exception as e:
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)
            

class UserInfoView(APIView):
    def get(self, request):
        try:
            user = request.user
            print("************", user)
            serializer = LoginSerializer(user)
            return Response({
                'data': serializer.data,
                'message': "User information retrieved successfully."
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)
        
# user post view
class PostView(APIView):
    permission_classes = [IsAuthenticated]  # if user is authenticated 
    authentication_classes = [JWTAuthentication]    # JWT token based autherntication
    
    # create a blog post
    def post(self, request):    
        try:
            data = request.data
            data['user'] = request.user.id  # requested user's id
            serializer = PostSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong."
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            
            return Response({
                'data': serializer.data,
                'message': "Blog created successfully."
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print("Exception:", e)
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)
            

class PostUpdateDelete(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, uid):
        try:
            blog = get_object_or_404(post, uid=uid)
            serializer = PostSerializer(blog)
            return Response({
                'data': serializer.data,
                'message': "Blog retrieved successfully."
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': "Blog not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid):
        try:
            data = request.data
            blog = get_object_or_404(post, uid=uid)
            
            # verify logged-in user and blog posted user.
            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': "You are not authorized to update this blog post."
                }, status=status.HTTP_403_FORBIDDEN)
                
            serializer = PostSerializer(blog, data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            
            return Response({
                'data': serializer.data,
                'message': "Blog Updated successfully."
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print("Exception:", e)
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        try:
            blog = get_object_or_404(post, uid=uid)
            
            # verify logged-in user and blog posted user.
            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': "You are not authorized to delete this blog post."
                }, status=status.HTTP_403_FORBIDDEN)
                
            blog.delete()
            return Response({
                'data': {},
                'message': "Blog Deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print("Exception:", e)
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)


class PublicPost(APIView):
    # get all blog post filter by user.
    def get(self, request):
        try:
            blogs = post.objects.all()
            serializer = PostSerializer(blogs, many=True)
            return Response({
                'data': serializer.data,
                'message': "Blogs fetched Successfullys."
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print("Exception:", e)
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
            
class LikeView(APIView):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(post, uuid=post_id)  # Filter post by uuid
            user = request.user
            
            # Check if the user has already liked the post
            if Like.objects.filter(post=post, user=user).exists():
                return Response({
                    'message': "You have already liked this post."
                }, status=status.HTTP_400_BAD_REQUEST)

            like = Like.objects.create(post=post, user=user)
            serializer = LikeSerializer(like)
            return Response({
                'data': serializer.data,
                'message': "Post liked successfully."
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            post = get_object_or_404(post, uuid=post_id)  # Filter post by uuid
            user = request.user
            
            # Check if the user has already liked the post
            like = Like.objects.filter(post=post, user=user).first()
            if not like:
                return Response({
                    'message': "You have not liked this post."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            like.delete()
            return Response({
                'message': "Post unliked successfully."
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': "Something went wrong."
            }, status=status.HTTP_400_BAD_REQUEST)