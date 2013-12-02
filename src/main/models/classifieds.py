# -*- coding: utf-8 -*-
import datetime, calendar, re
from django.db import models
from django.contrib.auth.models import User
from main.models.categories import ClassifiedCategory
from main.models.status import ClassifiedStatus
from main.models.locations import City, Province
from main.helpers import Upload

class Classified(models.Model):

    CLASSIFIED_EXPIRATION_MONTHS = 1

    CLASSIFIED_STATUS = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    CLASSIFIED_TYPES = (
        ('sale', 'For sale'),
        ('rent', 'For rent'),
    )
    CLASSIFIED_CURRENCIES = (
        ('', 'Select currency'),
        ('usd', 'Dollar'),
        ('peso_arg', 'Argentine Peso'),
    )

    def addMonths(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)

    @property
    def permalink(self, max_length = 45):
        title = re.sub('[^0-9a-zA-Z]+', ' ', self.title).strip()
        category = self.category.title.lower()
        return '%d/%s/%s' % (self.id, category, title[:max_length].lower().replace(' ', '-'))

    @property
    def image_1_thumbs(self):
        return Upload.getClasifiedThumbs(getattr(self, 'image_1'))

    @property
    def image_2_thumbs(self):
        return Upload.getClasifiedThumbs(getattr(self, 'image_2'))

    @property
    def image_3_thumbs(self):
        return Upload.getClasifiedThumbs(getattr(self, 'image_3'))

    def is_owner(self, user):
        owner = True
        if not self.user and not self.contact_email and not user:
            owner = False
        elif user != self.user and user.email != self.contact_email:
            owner = False
        return owner

    title = models.CharField(max_length = 255)
    content = models.TextField()
    user = models.ForeignKey(User, null = True, blank = True)
    category = models.ForeignKey(ClassifiedCategory)
    status = models.SmallIntegerField(max_length = 1, choices = CLASSIFIED_STATUS, default = 1)
    type = models.CharField(max_length = 12, choices = CLASSIFIED_TYPES, default = 'sale')
    currency = models.CharField(max_length = 12, choices = CLASSIFIED_CURRENCIES, default = 'peso_arg')
    created = models.DateTimeField(auto_now = True)
    expires = models.DateTimeField(default = addMonths(datetime.date.today(), CLASSIFIED_EXPIRATION_MONTHS))
    price = models.FloatField()
    
    city = models.ForeignKey(City, null = True, blank = True)
    contact_address = models.CharField(max_length = 128, null = True, blank = True)
    
    contact_name =  models.CharField(max_length = 64, null = True)
    contact_email = models.CharField(max_length = 128, null = True)
    contact_phone = models.CharField(max_length = 64, null = True, blank = True)
    google_map = models.CharField(max_length = 128, null = True, blank = True)
    visits = models.IntegerField(default = 0, null = True, blank = True)

    image_1 = models.ImageField(upload_to = Upload.generateRandomFilename('classifieds/images'), blank = True)
    image_2 = models.ImageField(upload_to = Upload.generateRandomFilename('classifieds/images'), blank = True)
    image_3 = models.ImageField(upload_to = Upload.generateRandomFilename('classifieds/images'), blank = True)

    class Meta:
        verbose_name_plural = 'Classifieds'
        app_label = 'main'
        db_table = 'main_classifieds'

    def __unicode__(self):
        return self.title