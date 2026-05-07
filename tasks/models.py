from django.db import models
from django.contrib.auth.models import User
from statuses.models import Status
from django.utils.translation import gettext_lazy as _



class Task(models.Model):
    name = models.CharField(
        _('Имя'), 
        max_length=150,
        unique=True
        )
    description = models.TextField(_('Описание'), blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT,
        verbose_name=_('Статус')
        )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name=_('Автор')
        )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='excepted_tasks',
        null=True,
        verbose_name=_('Исполнитель'))
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        'labels.Label',
        blank=True,
        related_name='tasks',
        verbose_name=_('Метка')
    )

    def __str__(self):
        return self.name