from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Trang chủ & xác thực người dùng
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    
    # CRUD Bài viết
    path('posts/', views.post_list, name="post_list"),  # Trang danh sách bài viết
    path('posts/create/', views.create_post, name="create_post"),
    path('posts/update/<int:id>/', views.update_post, name="update_post"),  # Trang chỉnh sửa bài viết
    path('posts/delete/<int:id>/', views.delete_post, name="delete_post"),  # Trang xóa bài viết
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]