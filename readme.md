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
