# coding: utf-8

from django.db import models


class School(models.Model):
    nominative = models.CharField('краткое имя школы', max_length=256)

    def __str__(self):
        return self.nominative


class Participant(models.Model):
    GENDER_CHOICES = (
        ('м', 'м'),
        ('ж', 'ж'),
    )

    version_code = models.CharField('код версии', max_length=32)
    participant_code = models.CharField('код участника', max_length=32)
    poll_code = models.CharField('код участника', max_length=32)
    test_number = models.CharField('номер работы', max_length=32)
    surname = models.CharField('фамилия', max_length=64)
    name = models.CharField('имя', max_length=64)
    gender = models.CharField('пол', max_length=1, choices=GENDER_CHOICES)
    grade = models.IntegerField('класс', default=6)
    school = models.ForeignKey(School, verbose_name='школа', blank=True, null=True)
    points_1 = models.IntegerField('1', blank=True, null=True)
    points_2a = models.IntegerField('2a', blank=True, null=True)
    points_2b = models.IntegerField('2b', blank=True, null=True)
    points_3 = models.IntegerField('3', blank=True, null=True)
    points_4 = models.IntegerField('4', blank=True, null=True)
    points_5 = models.IntegerField('5', blank=True, null=True)
    points_6 = models.IntegerField('6', blank=True, null=True)
    sum = models.IntegerField('сумма', blank=True, null=True)
