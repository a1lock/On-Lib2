from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Маршруты для страниц сайта
    path('', views.index_page, name='index'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('books/<int:book_id>/', views.book_detail_page, name='book_detail'),
    path('profile/', views.profile_page, name='profile'),

    # Маршруты для аутентификации
    path('register/', views.register_page, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]