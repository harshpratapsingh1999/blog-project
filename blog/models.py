from distutils.command.upload import upload
import email
from operator import mod
from statistics import mode
from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    date = models.DateField()
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    content = models.TextField(default="", blank=True, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to= "posts", null=True)
    def __str__(self) -> str:
        return f"{self.title} written by {self.author}"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs) 


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")



