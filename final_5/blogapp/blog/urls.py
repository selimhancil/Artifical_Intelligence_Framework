from django.urls import path
from . import views
from .views import MyProtectedView

urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),
    path("blogs", views.blogs, name="blogs"),
    path("category/<slug:slug>", views.blogs_by_category, name="blogs_by_category"),
    path("blogs/<slug:slug>", views.blog_details, name="blog_details"),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('comment/edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('protected/', MyProtectedView.as_view(), name='protected'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('about/', views.about, name='about'), 
]
