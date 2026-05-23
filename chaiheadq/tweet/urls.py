
from django.urls import path
from tweet import views
from .views import post_to_twitter



urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),
    path('detail/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/follow-toggle/', views.follow_toggle, name='follow_toggle'),
    path('tweet/<int:tweet_id>/like-toggle/', views.tweet_like_toggle, name='tweet_like_toggle'),
    path('register/', views.register, name='register'),
    #path('post/', post_to_twitter, name='post_tweet'),
    path('tweet/create/', views.tweet_create, name='tweet_create'),
      
]