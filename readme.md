# ptud-gk-de-1
### Huỳnh Hoàng Thuận-22673181
- bước 1 tạo môi trường
+ python version 3.11.0rc1
+ python -m venv myenv
+ myenv\Scripts\activate
- tạo folder 
+ django-admin startproject GK_PTUD
+ django-admin startapp app
- bước 2 cài đặt thư viện
+ pip install -r requirements
- bước 3 cài đặt database và đồng bộ với models.py

+ python manage.py migrate

+ python manage.py makemigrations

- tạo admin
+ python manage.py createsuperuser
- chạy 
+ python manage.py runserver
- các tác vụ có sẵn
+ vào trang /login /register
+ vào trang /posts để đăng tải bài viết
+ vào trang /dashboard để xem thôgn tin

### Mô tả 
- tạo base.html để lấy nav
- tạo 5 trang cho việc quản lý bài post thêm xóa sửa có phần text và hình ảnh
- tạo một trang dashboard để quản lý bài post có phần bình luận và thời gian đăng bài
- tạo trang register và login sau khi login có phần chào user/admin
- hiển thị các bài post dạng một cột 
- có đường dẫn trả về trang home
- không cho người dùng chưa đăng nhập xem được trang dashboard
