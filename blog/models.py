from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    job_title = models.CharField(max_length=200)
    
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(200)], null=False)
    description = models.TextField(validators=[MinLengthValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="blogs")
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    commented_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_user")
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return self.description