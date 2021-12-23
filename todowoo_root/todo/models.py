from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    status = (
        ('Срочно', 'Срочно'),
        ('Не срочно', 'Не срочно'),
        ('Очень срочно', 'Очень срочно'),
    )
    title = models.CharField(max_length=250, verbose_name='Задача')
    memo = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(max_length=250, verbose_name='Статус', choices=status)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, verbose_name='Крайний срок', blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
