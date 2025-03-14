from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from app.models import Post
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/home.html',context)

def register(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo Customer tự động khi đăng ký thành công
           

            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect("login")
        else:
            messages.error(request, "Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")

    context = {'form': form, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")  # Nếu user đã đăng nhập, chuyển về trang chủ

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:  # Kiểm tra trạng thái tài khoản
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.")
                return render(request, "app/login.html")  # QUAN TRỌNG: Render lại trang login để giữ thông báo
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")

    return render(request, "app/login.html")  # Render trang login

def logoutPage(request):
    logout(request)
    return redirect("login")

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Gán user hiện tại làm tác giả
            post.save()  # Gọi phương thức save của Post, tự động gán hình ảnh từ Picsum
            messages.success(request, "Bài viết đã được đăng thành công!")
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, 'app/create_post.html', {'form': form})



def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Lấy tất cả bài viết, sắp xếp mới nhất trước
    total_posts = posts.count()  # Đếm tổng số bài viết

    paginator = Paginator(posts, 10)  # Mỗi trang hiển thị 10 bài viết
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    posts_page = paginator.get_page(page_number)  # Lấy dữ liệu của trang hiện tại

    return render(request, 'app/post_list.html', {
        'posts': posts_page,  # Chỉ gửi dữ liệu của trang hiện tại
        'total_posts': total_posts,
    })



@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Bài viết đã được cập nhật!")
            return redirect("post_list")
    else:
        form = PostForm(instance=post)
    
    return render(request, 'app/update_post.html', {'form': form})


@login_required
def delete_post(request, id):
    # Lấy bài viết
    post = get_object_or_404(Post, id=id)

    # Kiểm tra quyền: Admin có thể xóa tất cả, user chỉ xóa bài của họ
    if request.user == post.author or request.user.is_superuser:
        if request.method == "POST":
            post.delete()
            messages.success(request, "Bài viết đã bị xóa!")
            return redirect("post_list")
    else:
        messages.error(request, "Bạn không có quyền xóa bài viết này!")
        return redirect("post_list")

    return render(request, 'app/delete_post.html', {'post': post})

@login_required
def members_list(request):
    # Lấy danh sách thành viên và đảm bảo user không bị mất liên kết
    members = Member.objects.select_related('user').all()

    for member in members:
        if member.user:  # Kiểm tra nếu user tồn tại
            member.post_count = Post.objects.filter(author=member.user).count()
        else:
            member.post_count = 0  # Nếu không có user, gán 0 bài viết

    return render(request, 'app/members.html', {'mem': members})
@login_required
def dashboard(request):
    # Lấy thông tin số lượng bài viết
    total_posts = Post.objects.count()
    
    # Lấy thông tin số lượng người dùng
    total_users = User.objects.count()
    
    # Lấy thông tin các bài viết gần đây (ví dụ: 5 bài gần nhất)
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    
    # Thông tin người dùng gần đây (ví dụ: 5 người dùng mới nhất)
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    return render(request, 'app/dashboard.html', {
        'total_posts': total_posts,
        'total_users': total_users,
        'recent_posts': recent_posts,
        'recent_users': recent_users
    })
    



@staff_member_required
def dashboard(request):
    # Lấy thông tin tổng quan
    total_posts = Post.objects.count()
    total_users = User.objects.count()
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    return render(request, 'app/dashboard.html', {
        'total_posts': total_posts,
        'total_users': total_users,
        'recent_posts': recent_posts,
        'recent_users': recent_users
    })
    
def post_detail(request, id):
    # Lấy bài viết với id cụ thể hoặc trả về 404 nếu không tìm thấy
    post = get_object_or_404(Post, id=id)
    
    return render(request, 'app/post_detail.html', {'post': post})