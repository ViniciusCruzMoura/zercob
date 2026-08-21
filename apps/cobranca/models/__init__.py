from django_celery_beat.apps import BeatConfig
from django_celery_results.apps import CeleryResultConfig
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask

BeatConfig.verbose_name = "Agendador"
CeleryResultConfig.verbose_name = "Execuções"
TaskResult._meta.verbose_name_plural = "Resultado das Tarefas"
TaskResult._meta.verbose_name='Resultado da Tarefa'
PeriodicTask._meta.verbose_name_plural = "Tarefas Agendadas"
PeriodicTask._meta.verbose_name = "Tarefa Agendada"
