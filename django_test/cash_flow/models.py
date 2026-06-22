from django.db import models
from django.utils import timezone


class Status(models.Model):
    status = models.TextField(null=False, blank=True, help_text="Статус ДДС")

    def __str__(self):
        return self.status


class Type(models.Model):
    type = models.TextField(null=False, blank=True, help_text="Тип ДДС")

    def __str__(self):
        return self.type


class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.TextField(null=False, blank=True, help_text="Категория ДДС")

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.TextField(
        null=False, blank=True, help_text="Подкатегория ДДС"
    )

    def __str__(self):
        return self.sub_category


class CashFlow(models.Model):
    created_at = models.DateField(
        default=timezone.now, help_text="Дата создания записи"
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, help_text="Подкатегория ДДС"
    )
    cash = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Итоговая сумма"
    )
    comments = models.TextField(null=True, blank=True, help_text="Комментарий")
