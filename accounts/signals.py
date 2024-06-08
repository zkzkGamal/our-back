from django.db.models.signals import post_save
from .models import Profile , Patient
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()

#create profile
@receiver(post_save , sender = User)
def create_profile(sender , instance , created, **kwargs):
    if created:
        name = instance.first_name + ' ' + instance.last_name
        profile = Profile.objects.create(user = instance , name = name , email = instance.email)
        Patient.objects.create(profile = profile)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
     if hasattr(instance, 'profile'):
        instance.profile.save()