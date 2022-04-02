from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Date(models.Model):
    day = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    month_number = models.CharField(
        blank=False,
        null=False,
        max_length=10,
        choices=(
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ),
    )
    fact = models.TextField(blank=False, null=False)


class Popular(models.Model):
    month_number = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=10,
        choices=(
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ),
    )
    days_checked = models.IntegerField(
        default=1,
        blank=False,
        null=False,
        validators=[
            MinValueValidator(1),
        ],
    )
