from django.db import models


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200
    )
    measure = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f'{self.title}, {self.measure}'
