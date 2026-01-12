from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('blog/<int:blog_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
