from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from parents.models import ParentProfile
from tutors.models import Tutor


def create_profile(sender, instance, created, **kwargs):
    if created:
        ParentProfile.objects.create(user=instance)
        instance.parentprofile.save()


post_save.connect(create_profile, sender=User)


def allow_user_become_tutor(sender, instance, created, **kwargs):
    if created:
        instance.profile.is_tutor = True
        instance.profile.save()


post_save.connect(allow_user_become_tutor, sender=Tutor)
