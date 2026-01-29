from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Author, Comment, Blog
from blog.projectApiKey.serializers import BlogSerialiser, AuthorSerializer, CommentSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from blog.projectApiKey.permissions import AdminOrReadOnly, IsCommentedUserOrReadOnly
from blog.projectApiKey import throttling
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from blog.projectApiKey.pagination import BlogPagination, AuthorPagination, BlogOffsetPagination, BlogCursorPagination
def home(request):
    return HttpResponse("blogs")

class AllAuthors(generics.ListAPIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [throttling.AllAuthorsThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    pagination_class = AuthorPagination
    throttle_scope = 'all-authors'
    filter_backends = [
    DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", 'email', 'job_title']
    search_fields = ["=name", "^email"]
    ordering_fields = ["name", "email"]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [AdminOrReadOnly]

class AuthorDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class CreateAuthor(generics.CreateAPIView):
    permission_classes = [AdminOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class AllBlogs(generics.ListAPIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [throttling.AllBlogsThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'all-blog'
    permission_classes = [AdminOrReadOnly]
    filter_backends = [
    DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", 'author__name']
    search_fields = ["^title", "=author__name"]
    ordering_fields = ["title"]
    serializer_class = BlogSerialiser
    queryset = Blog.objects.all()
    pagination_class = BlogCursorPagination

class Blog_create(generics.CreateAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Blog.objects.all()
    serializer_class = BlogSerialiser

class BlogDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", 'author__name']
    queryset = Blog.objects.all()
    serializer_class = BlogSerialiser

class AllComments(generics.ListAPIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [throttling.AllCommentsThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'all-comment'
    filter_backends = [
    DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["commented_user__username"]
    search_fields = ["commented_user_username"]
    ordering_fields = ["commented_user__username", "id"]
    serializer_class = CommentSerializer
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Comment.objects.filter(blog=pk)

class CreateComments(generics.CreateAPIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [throttling.CreateCommentThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'create-comment'
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        blog = Blog.objects.get(pk=pk)
        queryset = Comment.objects.filter(blog=blog, commented_user=self.request.user)
        if queryset.exists():
            raise ValidationError("You have already commented this blog. You can not submit another comment.")
        
        serializer.save(blog=blog, commented_user=self.request.user)
    
class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentedUserOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserComment(generics.ListAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(commented_user__username=username)
        return queryset


# class BlogDetails(APIView):
#     def get(self, request, pk):
#         try:
#             blog = Blog.objects.get(pk=pk)
#         except Blog.DoesNotExist:
#             return Response({"Error": "This blog does not exist."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = BlogSerialiser(blog)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         blog = Blog.objects.get(pk=pk)
#         serializer = BlogSerialiser(blog, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self, request, pk):
#         blog = Blog.objects.get(pk=pk)
#         blog.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class AllComments(APIView):
#     def get(self, request):
#         comments = Comment.objects.all()
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors)
 
# class CommentDetails(APIView):
#     def get(self, request, pk):
#         try:
#             comment = Comment.objects.get(pk=pk)
#         except Comment.DoesNotExist:
#             return Response({"Error": "This comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         comment = Comment.objects.get(pk=pk)
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         comment = Comment.objects.get(pk=pk)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)