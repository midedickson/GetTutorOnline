from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def upload_path(instance, filename):
    return '/'.join(['profile_photo', str(instance.user), filename])


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        serialize=True, null=True, blank=True, upload_to=upload_path)
    title = models.CharField(max_length=10)
    phone_number = models.CharField(
        verbose_name='Phone Number', max_length=14)
    address = models.CharField(max_length=200, verbose_name='Exact Address')
    local_govt = models.CharField(
        max_length=20, verbose_name='Local Government')
    state = models.CharField(max_length=20, verbose_name='State')
    is_tutor = models.BooleanField(default=False)

    # profile_photo

    def __str__(self):
        return f"{self.title} {self.user.first_name} {self.user.last_name}"
