from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Author(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    
    def update_rating(self):
        self.rating = 0
        for comment in Comment.objects.filter(user = self.user):
            self.rating += comment.rating

        for post in Post.objects.filter(author = Author.objects.get(user =self.user)):
            self.rating += post.rating * 3
            for comments_to_post in Comment.objects.filter(post = post):
                self.rating += comments_to_post.rating
        self.save()


class Category(models.Model):

    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
   
    NEWS = 'NS'
    POST = 'PT'
    POST_TYPE = [
        (NEWS, 'News'),
        (POST, 'Post'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=POST)
    pub_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Введите название')
    text = models.TextField(default='Введите содержание')
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating += -1
        self.save()
        
    def preview(self):
        return f'{self.text[0:124]}...'

    
class PostCategory(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Введите комментарий')
    pub_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating += -1
        self.save()