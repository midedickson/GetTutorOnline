from django.db import models
from parents.models import ParentProfile
# Create your models here.


class Tutor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    ID_CHOICES = (
        ('NIN', 'NIN'),
        ('PVC', 'Permanent Voters Card'),
        ('INTL', 'International Passport'),
        ('DRIV', 'Drivers\' License'),
    )
    profile = models.OneToOneField(ParentProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, default='M')
    age = models.CharField(max_length=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    disabilities = models.CharField(max_length=150, default='None', null=True, blank=True)
    nce = models.CharField(max_length=100, null=True, default='None', blank=True, verbose_name='College of Education')
    bachelors = models.CharField(
        max_length=200, default='None', null=True, blank=True, verbose_name='Bachelors')
    post_grad = models.CharField(
        max_length=100, null=True, default='None', blank=True, verbose_name='Post Graduate Studies')
    masters = models.CharField(
        max_length=200, default='None', null=True, blank=True, verbose_name='Masters')
    phd = models.CharField(max_length=100, default='None', null=True,
                           blank=True, verbose_name='Doctor of Philosophy(PhD)')
    government_id_type = models.CharField(
        choices=ID_CHOICES, max_length=4, null=True, blank=True)
    government_id_number = models.PositiveIntegerField(null=True, blank=True)
    yrs_of_experience = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.PositiveIntegerField(null=True, blank=True)
    bvn = models.PositiveIntegerField(null=True, blank=True)
    social_media_verification = models.BooleanField(default=False)
    government_id_verification = models.BooleanField(default=False)
    bank_verification = models.BooleanField(default=False)
    became_tutor_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.title} {self.profile.user.first_name} {self.profile.user.last_name}"


class Expertise(models.Model):
    GRADE_CHOICES = (
        ('primary', 'Primary'),
        ('juniors', 'Junior Secondary'),
        ('seniors', 'Senior Secondary'),
    )

    name = models.CharField(max_length=30)
    grade = models.CharField(choices=GRADE_CHOICES,
                             default='juniors', max_length=10)

    def __str__(self):
        return f"{self.name} for {self.grade}"


class TutoringPlan(models.Model):
    MEDIUM_CHOICES = (
        ('online', 'Online Tutoring'),
        ('physical', 'Physical Tutoring'),
        ('both', 'Online and Physical Tutoring'),
    )
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    major = models.ForeignKey(
        Expertise, on_delete=models.SET_NULL, null=True, related_name='major')
    minor1 = models.ForeignKey(
        Expertise, on_delete=models.SET_NULL, null=True, related_name='minor1')
    minor2 = models.ForeignKey(
        Expertise, on_delete=models.SET_NULL, null=True, related_name='minor2')
    desired_time = models.TimeField(null=True, blank=True)
    medium = models.CharField(
        max_length=10, choices=MEDIUM_CHOICES, default='online')
    locations = models.CharField(
        max_length=200, null=False, blank=False, default='Any Location...')
    first_hour_free = models.BooleanField(default=True)
    rate_per_hour = models.PositiveIntegerField(null=True, blank=True)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thur = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    mon_time = models.TimeField(null=True, blank=True)
    tue_time = models.TimeField(null=True, blank=True)
    wed_time = models.TimeField(null=True, blank=True)
    thur_time = models.TimeField(null=True, blank=True)
    fri_time = models.TimeField(null=True, blank=True)
    sat_time = models.TimeField(null=True, blank=True)
    sun_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        tutor = self.tutor.profile
        return f"{tutor.title} {tutor.user.first_name} {tutor.user.last_name}'s Tutoring Plan"
