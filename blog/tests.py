from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from blog.projectApiKey.serializers import BlogSerialiser, CommentSerializer, AuthorSerializer
from blog.models import Blog, Author, Comment

class BlogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="dave@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(name="dave", email="dave@123")
        self.blog = Blog.objects.create(
        title="Digital Marketing", description="I love digital Marketing and a lot of more things related", author=self.author)
        
    def test_createBlog(self):
        data ={
            "title":"Digital marketing",
            "description":"I love digital Marketing and a lot of more things related",
            "author":self.user
        }
        
        response = self.client.post(reverse("create-blog"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_deleteBlog(self):
        response = self.client.delete(reverse("blog-details", args=(self.blog.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_individual_blog(self):
        response = self.client.get(reverse("blog-details", args=(self.blog.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getListBlog(self):
        response = self.client.get(reverse("all-blogs"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updateBlog(self):
        data ={
            "title":"Digital marketing!!",
            "description":"I love digital Marketing and a lot of more things related",
            "author":self.user
        }
        
        response = self.client.post(reverse("blog-details", args=(self.blog.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="dave@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(name="dave", email="dave@123")
        self.blog1 = Blog.objects.create(
        title="Digital Marketing", 
        description="I love digital Marketing and a lot of more things related",
        author=self.author)
        
        self.comment1 = Comment.objects.create(
            commented_user=self.user, 
            description="I like this Blog!!", blog=self.blog1)
        
        self.blog = Blog.objects.create(
        title="Digital Marketing", 
        description="I love digital Marketing and a lot of more things related", 
        author=self.author)
    
    def test_createComment(self):
        data = {
            "commented_user":self.user,
            "description":"Amazing Blog",
            "blog":self.blog
        }
        
        response = self.client.post(reverse("create-comment", args=(self.blog.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_deleteComment(self):
        response = self.client.delete(reverse("comment_details", args=(self.comment1.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_singleComment(self):
        response = self.client.get(reverse("comment_details", args=(self.comment1.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_allComments(self):
        response = self.client.get(reverse("comments", args=(self.blog.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updateComment(self):
        data = {
            "commented_user":self.user,
            "description":"Amazing Blog@@2",
            "blog":self.blog
        }
        
        response = self.client.put(reverse("comment_details", args=(self.comment1.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_comment_non_auth_user(self):
        data = {
            "commented_user":self.user,
            "description":"Amazing Blog@@2",
            "blog":self.blog
        }
        
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(reverse("create-comment", args=(self.blog1.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="son", password="son!123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(name="dave", email="dave@123")
    
    def test_createAuthor(self):
        data = {
            "name":"dave",
            "email":"dave@123"
        }
        
        response = self.client.post(reverse("create-author"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_deleteAuthor(self):
        response = self.client.delete(reverse("author-details", args=(self.author.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_getlistAuthors(self):
        response = self.client.get(reverse("all-authors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updateAuthor(self):
        data = {
            "name":"david",
            "email":"dave@gmail.123.com"
        }
        
        response = self.client.put(reverse("author-details", args=(self.author.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_singleAuthor(self):
        response = self.client.get(reverse("author-details", args=(self.author.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_userComment(self):
        response = self.client.get("/usercomment/?username=" + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)