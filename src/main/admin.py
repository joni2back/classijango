# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Classified, ClassifiedCategory, ClassifiedStatus
from main.models import City, Province, Country

admin.site.register(Classified)
admin.site.register(ClassifiedCategory)
admin.site.register(ClassifiedStatus)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)

