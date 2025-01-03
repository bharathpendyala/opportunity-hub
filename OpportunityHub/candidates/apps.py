from django.apps import AppConfig


class JobseekersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OpportunityHub.candidates'

    def ready(self):
        import OpportunityHub.candidates.signals
