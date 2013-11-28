# -*- coding: utf-8 -*-
from django.db import models
import re

class ClassifiedCategory(models.Model):

    title = models.CharField(max_length = 200)
    content = models.TextField(blank = True)

    @property
    def permalink(self, max_length = 75):
        title = re.sub('[^0-9a-zA-Z]+', ' ', self.title).strip()
        return '%s' % title[:max_length].lower().replace(' ', '-')

    class Meta:
        verbose_name_plural = 'Classifieds Categories'
        app_label = 'main'
        db_table = 'main_classifieds_categories'



    def __unicode__(self):
        return self.title



       