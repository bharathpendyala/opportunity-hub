from django.contrib.auth import get_user_model
from django.db import models

from OpportunityHub.jobs.models import Job
from OpportunityHub.candidates.models import Candidate

UserModel = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='candidate')
    message = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class NotificationCandidate(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    comment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]