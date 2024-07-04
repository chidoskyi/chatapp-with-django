from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from .models import StoryStream
from django.http import JsonResponse
from stories.models import Story, StoryStream
from stories.forms import NewStoryForm
from  datetime import datetime, timedelta

@login_required
def NewStory(request):
    user = request.user

    if request.method == "POST":
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Story object with the user, content, and caption
            story = Story(
                user=user, 
                content=form.cleaned_data['content'], 
                caption=form.cleaned_data['caption']
            )
            story.save()
            return redirect('index')  # Redirect to the index page after saving
    else:
        form = NewStoryForm()  # If GET request, render an empty form

    context = {
        'form': form
    }
    
    return render(request, 'newstory.html', context)  # Render the form in the template

from django.http import JsonResponse

# def ShowMedia(request, stream_id):
#     stories_stream = get_object_or_404(StoryStream, id=stream_id)
#     media_stories = stories_stream.story.all().values()  # Adjust fields as per your model
#     stories_list = list(media_stories)
#     return JsonResponse(stories_list, safe=False)


# @login_required
# def story_feed(request):
#     user = request.user
#     stories = Story.objects.all().order_by('-posted')
#     context = {
#         'stories': stories,
#         'user': user,
#     }
#     return render(request, 'index2.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

def ShowMedia(request, status_id):
    story = get_object_or_404(Story, id=status_id)
    return JsonResponse({'content': story.content.url})  # Return URL of the status content (image or video)

@login_required
def story_feed(request):
    user = request.user
    stories = Story.objects.filter(user=user).order_by('-posted')  # Fetch only current user's statuses
    context = {
        'stories': stories,
        'user': user,
    }
    return render(request, 'index2.html', context)

