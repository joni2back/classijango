# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Classified, ClassifiedCategory, ClassifiedStatus

admin.site.register(Classified)
admin.site.register(ClassifiedCategory)
admin.site.register(ClassifiedStatus)
