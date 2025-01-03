from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OpportunityHub.notifications'

    def ready(self):
        import OpportunityHub.notifications.signals