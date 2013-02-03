from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    genitiv = models.CharField(max_length=256)


class Participant(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )

    number = models.CharField(max_length=32)
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grade = models.IntegerField()
    school = models.ForeignKey(School)
#    points = models.CommaSeparatedIntegerField(max_length=64)
#    points_1 = models.IntegerField()
#    points_2 = models.IntegerField()
#    points_3 = models.IntegerField()
#    points_4 = models.IntegerField()
#    points_5 = models.IntegerField()
#    points_6 = models.IntegerField()
