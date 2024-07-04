from django.db import models
from django.db.models import Max
from userauths.models import User



class Messages(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    body = models.TextField(null=True)
    date = models.DateTimeField( auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def sender_message(from_user, to_user, body):
        sender_message = Messages(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
        )
        
        sender_message.save()
        
        recipient_message = Messages(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body,
            is_read=True
        )
        recipient_message.save()   
        
        return sender_message
    
    @staticmethod
    def get_message(user):
        
        messages = Messages.objects.filter(user=user).values("recipient").annotate(last=Max("date")).order_by('-last')
        users = []
        
        for message in messages:
            recipient  =  User.objects.get(pk=message["recipient"])
            unread = Messages.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            
            users.append({
                'user': recipient,
                "last": message['last'],
                'unread': unread
            })
        return users
    
    
class Topic(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return self.name
    


class Room(models.Model):
    image = models.ImageField(upload_to='rooms-images', default='room.png')
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        
        
    def __str__(self):
        return self.topic.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Room Message'
        verbose_name_plural = 'Room Messages'
        
    def __str__(self):
        return self.user.username