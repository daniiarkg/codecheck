from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Coder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fio = models.CharField(verbose_name='ФИО', max_length=200, null=True)


# Create your models here.
class Task(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200, null=True)
    description = models.TextField(verbose_name='Описание задания', null=True)
    published_by = models.ForeignKey(Coder, on_delete=models.CASCADE, verbose_name='Автор', null=True)
    source_code = models.TextField(verbose_name='Исходный код', null=True)
    date = models.DateTimeField(verbose_name='Создано', default=timezone.now)


class TaskComplete(models.Model):
    coder = models.ForeignKey(Coder, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    code = models.TextField(verbose_name='Код решения', null=True)
    date = models.DateTimeField(verbose_name='Решено', default=timezone.now)