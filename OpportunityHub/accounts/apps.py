from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OpportunityHub.accounts'

    def ready(self):
        import OpportunityHub.accounts.signals
