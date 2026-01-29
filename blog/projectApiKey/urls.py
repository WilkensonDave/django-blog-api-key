from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.projectApiKey import views

# router = DefaultRouter()
# router.register("authors", views.AllAuthors, basename="authors")
# router.register("blogs", views.AllBlogs, basename="blogs")


urlpatterns = [
    path("blogs/<int:pk>/create/", views.CreateComments.as_view(), name="create-comment"),
    path("blogs/<int:pk>/comments/", views.AllComments.as_view(), name="comments"),
    path("blogs/comment/<int:pk>", views.CommentDetails.as_view(), name="comment_details"),
    path("createblog/", views.Blog_create.as_view(), name="create-blog"),
    path("allauthors/", views.AllAuthors.as_view(), name="all-authors"),
    path("authordetails/<int:pk>/", views.AuthorDetails.as_view(), name="author-details"),
    path("createauthor/", views.CreateAuthor.as_view(), name="create-author"),
    path("allblogs/", views.AllBlogs.as_view(), name="all-blogs"),
    path("blogdetails/<int:pk>/", views.BlogDetails.as_view(), name="blog-details"),
    path("usercomment/", views.UserComment.as_view(), name="user-comment"),
]
