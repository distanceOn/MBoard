"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from my_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register, name='register'),
    path('create_advertisement/', views.create_advertisement, name='create_advertisement'),
    path('view_advertisement/<int:ad_id>/', views.view_advertisement, name='view_advertisement'),
    path('edit_advertisement/<int:ad_id>/', views.edit_advertisement, name='edit_advertisement'),
    path('create_response/<int:ad_id>/', views.create_response, name='create_response'),
    path('view_responses/', views.view_responses, name='view_responses'),
    path('email_sent/', views.email_sent, name='email_sent'),
    path('confirm_email_page/', views.confirm_email_page, name='confirm_email_page'),
    path('home/', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(next_page='home'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('manage_response/<int:response_id>/<str:action>/', views.manage_response, name='manage_response'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
