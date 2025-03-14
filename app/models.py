from django.db import models
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import random

# Create your models here.
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.CharField(max_length=255, null=True, blank=True)  # Lưu URL của hình ảnh
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Tạo URL hình ảnh random từ Picsum nếu chưa có
        if not self.image_url:
            self.image_url = f"https://picsum.photos/500/300?random={random.randint(1, 1000)}"
        super(Post, self).save(*args, **kwargs)  # Gọi phương thức save của class cha

    def __str__(self):
        return self.title
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)

    def post_count(self):
        if self.user:
            return self.user.post_set.count()
        return 0