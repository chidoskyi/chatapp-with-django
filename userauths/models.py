from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    bio = models.CharField(max_length=150, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self) -> str:
        return self.username


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

 
class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField( max_length=150)
    bio = models.CharField( max_length=150)
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg')
    website = models.URLField(default="https://website.com")
    facebook = models.URLField(default="https://facebook.com")
    instagram = models.URLField(default="https://instagram.com")
    twitter = models.URLField(default="https://twitter.com")
    
    def __str__(self):
        
        try:
            return f"{self.full_name} - {self.user.username} - {self.user.email}"
        except:
            return self.user.username
        
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
                
                
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profiles.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)