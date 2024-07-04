from django.urls import path
from . import views
from stories.views import NewStory,ShowMedia

urlpatterns = [
    path('new_story/', views.NewStory, name='new_story'),
    path('show_media/<int:stream_id>/', views.ShowMedia, name='show_media'),
    path('story_feed/', views.story_feed, name='story_feed'),
]