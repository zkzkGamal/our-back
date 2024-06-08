from django.db import models
from accounts.models import Profile
# Create your models here.


# Create your models here.
class message_response(models.Model):
    message = models.CharField(max_length = 100)
    response = models.CharField(max_length = 500)

    def __str__(self):
        return self.message
    
# Create your models here.
class message_responsa(models.Model):
    message = models.CharField(max_length = 100)
    response = models.CharField(max_length = 500)

    def __str__(self):
        return self.message

class AI_Messages(models.Model):
    session_id = models.CharField(max_length=20)
    sender_message = models.TextField(null=True,blank=True)
    bot_message = models.TextField()
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # ForeignKey relationship
    bot_message_image = models.ImageField(upload_to='media/bot_messages' , null=True, blank=True)
    message_image = models.ImageField(upload_to='media/user_toBot_messages' , null=True, blank=True)

    def __str__(self):
        return self.profile.name
