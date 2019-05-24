from django.core.validators import EmailValidator
from django.db import models
from datetime import datetime

MEASURES = (
    (1, "kg"),
    (2, "l"),
    (3, "szt"),
    (4, "op."),
)

GROUPS = (
    (1, "Zbożowe"),
    (2, "Mleczne"),
    (3, "Jaja"),
    (4, "Mięsne"),
    (5, "Masło"),
    (6, "Inne tłuszcze"),
    (7, "Ziemniaki"),
    (8, "Warz. i owoce z wit. C"),
    (9, "Warz. i owoce z karot."),
    (10, "Inne warzywa i owoce"),
    (11, "Strączkowe suche"),
    (12, "Cukier i słodycze"),
)

TYPES = (
    (1, "Przyjęcie"),
    (2, "Wydanie"),
)


class School(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=40, validators=[EmailValidator()])


class Menu(models.Model):
    date = models.DateField(blank=False)
    name = models.CharField(max_length=255, null=False)
    inventory = models.ManyToManyField('Inventory')

    # def __str__(self):
    #     return self.name


class Products(models.Model):
    name = models.CharField(max_length=64, null=False)
    unit = models.IntegerField(choices=MEASURES, null=False)
    calories = models.IntegerField(null=True)
    protein = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    carbo = models.FloatField(null=True)
    calcium = models.IntegerField(null=True)
    iron = models.FloatField(null=True)
    vit_A = models.IntegerField(null=True)
    vit_B1 = models.FloatField(null=True)
    vit_B2 = models.FloatField(null=True)
    vit_C = models.FloatField(null=True)
    group = models.IntegerField(choices=GROUPS, null=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    operation_date = models.DateField(blank=False)
    operation_type = models.IntegerField(choices=TYPES, null=False)
    quantity = models.FloatField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    product = models.ForeignKey(Products, on_delete=True)
