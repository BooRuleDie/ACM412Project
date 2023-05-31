from django.urls import path
from .views import Login, Signup, Home, Profile, TopicView, HandleModalSubmits

urlpatterns = [
    path('login/', Login, name='login'),
    path('signup/', Signup, name='signup'),
    path('', Home, name='home'),
    path('profile/<str:user_id>/', Profile, name='profile'),
    path('topic/<str:topic_id>/', TopicView, name='topic'),
    path('handlemodalsubmit/', HandleModalSubmits, name='handlemodalsubmit'),
]
