from django.apps import AppConfig


class CobrancaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cobranca'
    verbose_name = "Solfacil"

    icon = 'fa fa-square-poll-vertical'  # FontAwesome icon for the app (optional)
    divider_title = "Cobrança"  # Title of the section divider in the sidebar (optional)
    priority = 0  # Determines the order of the app in the sidebar (higher values appear first, optional)
    hide = False  # Set to True to hide the app from the sidebar menu (optional)
