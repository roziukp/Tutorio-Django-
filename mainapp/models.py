from django.db import models
from django.contrib.auth.forms import User
from datetime import datetime
from django.utils import timezone
from mptt.models import TreeForeignKey, MPTTModel
import mptt

class Profile(models.Model):

    def get_file_path(self, filename):
        return '{}/{}'.format(datetime.strftime(datetime.now(), '%Y_%m_%d'), filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='User name')
    surname = models.CharField(max_length=100, verbose_name='User surname')
    telephone = models.CharField(max_length=10, blank=False, verbose_name='User telephone')
    email = models.EmailField()
    profile_img = models.ImageField(upload_to=get_file_path, blank=True, null=True, verbose_name='Profile Image')

    def __str__(self):
        return "{} {}".format(self.name, self.surname)


class CV(models.Model):
    cv = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    education = models.CharField(max_length=256, verbose_name='User education', null=False, blank=False)
    experience = models.IntegerField(verbose_name='Experience(years)', null=False, blank=False)
    subject = models.CharField(max_length=100, verbose_name='Subject', null=False, blank=False)
    extra_info = models.TextField(verbose_name='Extra user information', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['-creation_date']


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

mptt.register(Category, order_insertion_by=['name'])

class Post(models.Model):
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return 'Comment for: {}'.format(self.body)

mptt.register(Comment, order_insertion_by=['created_at'])
