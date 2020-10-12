from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def upload_path(instance, filename):
    return '/'.join(['profile_photo', str(instance.user), filename])


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        serialize=True, null=True, blank=True, upload_to=upload_path)
    title = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(
        verbose_name='Phone Number', max_length=14, blank=True, null=True)
    address = models.CharField(
        max_length=200, verbose_name='Exact Address', blank=True, null=True)
    local_govt = models.CharField(
        max_length=20, verbose_name='Local Government', blank=True, null=True)
    state = models.CharField(
        max_length=20, verbose_name='State', blank=True, null=True)
    is_tutor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.user.first_name} {self.user.last_name}"


class TutorRequest(models.Model):
    MEDIUM_CHOICES = (
        ('online', 'Online Tutoring'),
        ('physical', 'Physical Tutoring'),
        ('both', 'Both'),
    )
    requested_tutorplan = models.OneToOneField(
        'tutors.TutoringPlan', on_delete=models.CASCADE, related_name='tutor_request')
    subjects_requested = models.ManyToManyField('tutors.Expertise')
    medium = models.CharField(
        max_length=10, choices=MEDIUM_CHOICES, default='online')
    requested_by = models.ForeignKey(
        ParentProfile, on_delete=models.CASCADE, related_name='tutor_request')
    hour_per_day = models.PositiveIntegerField(verbose_name='Hours Per Day')
    days_per_week = models.PositiveIntegerField(verbose_name='Days Per Week')
    requested_duration = models.PositiveIntegerField(
        verbose_name='Weeks_Needed')
    location_needed = models.CharField(
        max_length=200, verbose_name='Tutoring_Location')
    description = models.TextField(max_length=1000, blank=True, null=True)
    purpose_of_cancellation = models.TextField(
        max_length=1000, blank=True, null=True)
    isAccepted = models.BooleanField(default=False)
    inProgress = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)
    isCancelled = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)

    @property
    def get_total_price(self):
        price_per_day = float(self.requested_tutorplan.rate_per_hour *
                              self.hour_per_day)
        price_per_week = float(price_per_day * self.days_per_week)
        total_price = float(price_per_week * self.requested_duration)
        return total_price

    @property
    def get_tutor(self):
        tutor = self.requested_tutorplan.tutor
        return tutor

    def __str__(self):
        return f"{self.requested_tutorplan.__str__()}"
