# from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug= models.SlugField(max_length=200)
    bio = models.CharField(max_length=140, blank=True)
    avatar = models.ImageField(upload_to='images/profile', default=None, blank=True)
    dob= models.DateField(null=True, blank=True)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
          