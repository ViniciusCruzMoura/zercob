from django.urls import path
from apps.lgpd.views import send_message_pliq, dashboard_redirect_to_lgpd

app_name = 'lgpd'

urlpatterns = [
        path('lgpd/sebraeparceiro/<str:cgc_cpf>/pliq/send', send_message_pliq, name='send_message_pliq'),
        path('', dashboard_redirect_to_lgpd, name='dashboard_redirect_to_lgpd'),
        ]

