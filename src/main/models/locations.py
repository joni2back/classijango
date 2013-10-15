# -*- coding: utf-8 -*-
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length = 96)
    class Meta:
        verbose_name_plural = 'Countries'
        app_label = 'main'
        db_table = 'main_location_countries'

    def __unicode__(self):
        return self.name.title()

class Province(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length = 96)

    class Meta:
        verbose_name_plural = 'Provinces'
        app_label = 'main'
        db_table = 'main_location_provinces'

    def __unicode__(self):
        return self.name.title()

class City(models.Model):
    name = models.CharField(max_length = 96)
    cp = models.IntegerField(max_length = 8)
    province = models.ForeignKey(Province)
    google_map = models.CharField(max_length = 32, null = True, blank = True)

    class Meta:
        verbose_name_plural = 'Cities'
        app_label = 'main'
        db_table = 'main_location_cities'

    def __unicode__(self):
        return self.name.title()