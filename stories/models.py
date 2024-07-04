from django.db import models
from django.contrib.auth.models import User
from chatapp.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
def user_directory_path(instance, filename):
    #file will be uploaded to MEDIA_ROOT/ user<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
    content = models.FileField(upload_to=user_directory_path)
    caption = models.TextField(max_length=50)
    expired = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        # return self.user.username
        return f"{self.user.username}'s Stories"
    
    
class StoryStream(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='story_streams')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='stories')
    date = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.following.username + ' - ' + str(self.date)
    def __str__(self):
        return f"{self.user.username} - {self.story.user.username} - {self.date}"
    
@receiver(post_save, sender=Story)
def add_to_story_stream(sender, instance, created, **kwargs):
    if created:
        new_story = instance
        users = User.objects.exclude(id=new_story.user.id)
        
        for user in users:
            StoryStream.objects.create(user=user, story=new_story)

#Story Stream
# post_save.connect(StoryStream.add_post, sender=Story) 


    

    
    