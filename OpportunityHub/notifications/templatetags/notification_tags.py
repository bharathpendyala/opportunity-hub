from django import template
from OpportunityHub.notifications.models import NotificationCandidate, Notification

register = template.Library()


@register.filter
def unread_notifications(user):
    if user.role == "candidate":
            return len(NotificationCandidate.objects.filter(user=user, is_read=False))
    elif user.role == "company":
            return len(Notification.objects.filter(user=user, is_read=False))
    else:
        return 0
    