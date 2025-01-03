from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from OpportunityHub.jobs.models import Applicant, Skills
from OpportunityHub.core.validators import validate_phone_number, validate_start_with_upper
 

UserModel = get_user_model()

GENDER_TYPE = (
    ('M', "Male"),
    ('F', "Female"),
)

class Candidate(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, blank=False, null=False, validators=[validate_start_with_upper], verbose_name="First Name")
    last_name = models.CharField(max_length=50, blank=False, null=False, validators=[validate_start_with_upper])
    city = models.CharField(max_length=50, blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=False, null=False)
    occupation = models.CharField(max_length=50, blank=False, null=False)
    website = models.URLField(max_length=70, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True, max_length=50)
    facebook = models.URLField(blank=True, null=True, max_length=50)
    github = models.URLField(blank=True, null=True, max_length=50)
    about = RichTextField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, blank=True, null=True, validators=[validate_phone_number])
    # profile_picture = models.ImageField(
    #     blank=True, null=True, upload_to='images/profile')
    profile_picture = CloudinaryField('image', blank=True, null=True)
    gender = models.CharField(blank=False, null=False,
                              choices=GENDER_TYPE, max_length=1)

    skills = models.ManyToManyField(Skills, related_name="skills")
    activated = models.BooleanField(default=False)

    @property
    def get_user_all_applicant(self):
        return Applicant.objects.filter(user=self.user).count()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return str(self.user)

    class Meta:
        ordering = ['-pk']


class Education(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations')
    image = models.URLField(max_length=200, blank=True, null=True)
    institution = models.CharField(max_length=100)
    description = RichTextField(max_length=200)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'start_date': 'Start date cannot be after end date.'})

    def __str__(self):
        return self.institution


class Experience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='experience')
    image = models.URLField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=100)
    description = RichTextField(max_length=500)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def clean(self):

        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'start_date': 'Start date cannot be after end date.'})

    def __str__(self):
        return self.company

 
class CandidateCVs(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="cvs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_cvs")
    file = models.FileField(upload_to="cvs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        unique_together = ["applicant", "job"]

    def __str__(self):
        return f"CV of {self.applicant.user.username} for {self.job.title}"

        
class Award(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="awards")
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    reward = models.CharField(max_length=255)
    more_information = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.reward} at {self.location} ({self.start_year} - {self.end_year})"
