from django.apps import AppConfig


class UserAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_admin'
    label = 'app_user_admin'
    verbose_name = "user_admin"

    def ready(self):
        import apps.user_admin.signals
