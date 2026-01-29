from blog.admin import Author, Comment, Blog
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    commented_user = serializers.StringRelatedField(read_only=True)
    class Meta:  
        model = Comment
        exclude = ("blog", )
        
class BlogSerialiser(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.CharField(source="author.name")
    class Meta:
        model = Blog
        exclude = ['description']

class AuthorSerializer(serializers.ModelSerializer):
    blogs = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True,
        view_name="blog-details"
    )
    class Meta:
        model = Author
        fields = "__all__"



