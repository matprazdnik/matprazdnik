# coding: utf-8

from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField('номер/название', max_length=64)
    city = models.CharField('город', max_length=64, default='Москва')
    genitive = models.CharField('полное название в родительном падеже', max_length=256)

    def __str__(self):
        return '{0}, {1}: {2}'.format(self.name, self.city, self.genitive)

    @property
    def name_and_city(self):
        return '{0}, {1}'.format(self.name, self.city)


class Participant(models.Model):
    GENDER_CHOICES = (
        ('м', 'м'),
        ('ж', 'ж'),
    )

    number = models.CharField('номер', max_length=32)
    surname = models.CharField('фамилия', max_length=64)
    name = models.CharField('имя', max_length=64)
    gender = models.CharField('пол', max_length=1, choices=GENDER_CHOICES)
    grade = models.IntegerField('класс', default=6)
    school = models.ForeignKey(School, verbose_name='школа', blank=True, null=True)
    # points = models.CommaSeparatedIntegerField(max_length=64)
    points_1 = models.IntegerField('1', blank=True, null=True)
    points_2 = models.IntegerField('2', blank=True, null=True)
    points_3 = models.IntegerField('3', blank=True, null=True)
    points_4 = models.IntegerField('4', blank=True, null=True)
    points_5 = models.IntegerField('5', blank=True, null=True)
    points_6a = models.IntegerField('6а', blank=True, null=True)
    points_6b = models.IntegerField('6б', blank=True, null=True)
    sum = models.IntegerField('сумма', blank=True, null=True)
