from django.urls import path
from .views import Login, Signup, Home, Profile, TopicView, HandleModalSubmits, TopicList, SearchTopicList, ProfileTopicList, CommentTopicList, UpvoteDownvote

urlpatterns = [
    path('login/', Login, name='login'),
    path('signup/', Signup, name='signup'),
    path('', Home, name='home'),
    path('profile/<str:user_id>/', Profile, name='profile'),
    path('topic/<str:topic_id>/', TopicView, name='topic'),
    path('handlemodalsubmit/', HandleModalSubmits, name='handlemodalsubmit'),

    # APIs
    path('api/topic/<int:start_index>/<int:end_index>/', TopicList.as_view(), name="topic-list-api"),
    path('api/topic/<str:user_id>/<int:start_index>/<int:end_index>/', ProfileTopicList.as_view(), name="profile-topic-list-api"),
    path('api/search/<str:search>/', SearchTopicList.as_view(), name="search-topic-api"),
    path('api/comment/<str:topic_id>/<int:start_index>/<int:end_index>/', CommentTopicList, name="comment-topic-list"),
    path('api/vote/<str:option>/<str:comment_id>/', UpvoteDownvote, name="upvote-downvote"),

]
