# -*- coding: utf-8 -*-
from django.db import models

class ClassifiedCategory(models.Model):
	title = models.CharField(max_length = 200)
	content = models.TextField(blank = True)

	class Meta:
		verbose_name_plural = 'Classifieds Categories'
		app_label = 'main'
		db_table = 'main_classifieds_categories'

	def __unicode__(self):
		return self.title
