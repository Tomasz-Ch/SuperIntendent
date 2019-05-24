"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from superintendent.views import StartView, NewMenuView, MenuView, SchoolUpdate, AllProductsView, AddProductView, \
    ModifyProductUpdate, ProductView, InvoiceView, UsedView, ReportView, LoginView, SearchProductView, AddUserView, \
    ListUsersView, ResetPasswordView, emailView, successView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', StartView.as_view(), name="index"),
    path('new_menu/', NewMenuView.as_view(), name="new-menu"),
    path('obiady/', MenuView.as_view(), name="obiady"),
    path('szkola/<pk>', SchoolUpdate.as_view(), name="school"),
    url(r'^all_products/', AllProductsView.as_view(), name="all-products"),
    url(r'^add_product/', AddProductView.as_view(), name="add-product"),
    path('edit_product/<pk>', ModifyProductUpdate.as_view(), name="edit-product"),
    url(r'^product/(?P<product_id>(\d)+)', ProductView.as_view(), name="product-detail"),
    url(r'^invoice/', InvoiceView.as_view(), name="invoice"),
    url(r'^used/', UsedView.as_view(), name="used"),
    url(r'^report/', ReportView.as_view(), name="report"),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('product_search/', SearchProductView.as_view(), name="product-search"),
    url(r'add_user/', AddUserView.as_view(), name='add-user'),
    url(r'list_users/', ListUsersView.as_view(), name='list-users'),
    url(r'reset_password/', ResetPasswordView.as_view(), name='reset-password'),
    url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>'
        r'[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('email/', emailView, name='email'),
    path('success/', successView, name='success'),
]
