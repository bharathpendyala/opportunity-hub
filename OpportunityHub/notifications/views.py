from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, View

from OpportunityHub.notifications.models import NotificationCandidate, Notification


class CandidateNotificationListView(LoginRequiredMixin, ListView):
    model = NotificationCandidate
    template_name = 'candidates/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MarkNotificationAsReadView(View):
    def get(self, request, *args, **kwargs):
        notification_id = self.kwargs['pk']
        notification = NotificationCandidate.objects.get(pk=notification_id)
        notification.is_read = not notification.is_read
        notification.save()
        return redirect('job seeker notifications')



class CompanyNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'company/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MarkCompanyNotificationAsReadView(View):
    def get(self, request, *args, **kwargs):
        notification_id = self.kwargs['pk']
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = not notification.is_read
        notification.save()
        return redirect('company-notifications')