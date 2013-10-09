import datetime, calendar
from django.db import models
from django.contrib.auth.models import User
from main.models.categories import ClassifiedCategory
from main.models.status import ClassifiedStatus
from main.models.locations import City, Province
from main.helpers import Upload

class Classified(models.Model):

    CLASSIFIED_EXPIRATION_MONTHS = 1

    CLASSIFIED_STATUS = (
        (0, 'Inactivo'),
        (1, 'Activo'),
    )
    CLASSIFIED_TYPES = (
        ('sale', 'En venta'),
        ('rent', 'En alquiler'),
    )
    CLASSIFIED_CURRENCIES = (
        ('usd', 'Dolares'),
        ('peso_arg', 'Pesos Arg'),
    )

    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)

    expirationDate = add_months(datetime.date.today(), CLASSIFIED_EXPIRATION_MONTHS)

    title = models.CharField(max_length = 255)
    content = models.TextField()
    user = models.ForeignKey(User, null = True, blank = True)
    category = models.ForeignKey(ClassifiedCategory)
    status = models.SmallIntegerField(max_length = 1, choices = CLASSIFIED_STATUS, default = 1)
    type = models.CharField(max_length = 12, choices = CLASSIFIED_TYPES, default = 'sale')
    currency = models.CharField(max_length = 12, choices = CLASSIFIED_CURRENCIES, default = 'peso_arg')
    created = models.DateTimeField(auto_now = True)
    expires = models.DateTimeField(default = expirationDate)
    price = models.FloatField()
    
    city = models.ForeignKey(City, null = True, blank = True)
    contact_address = models.CharField(max_length = 128, null = True, blank = True)
    
    contact_name =  models.CharField(max_length = 64, null = True)
    contact_email = models.CharField(max_length = 128, null = True)
    contact_phone = models.CharField(max_length = 64, null = True, blank = True)
    google_map = models.CharField(max_length = 128, null = True, blank = True)

    image_1 = models.ImageField(upload_to = Upload.random_file_name('classifieds/images'), blank = True)
    image_2 = models.ImageField(upload_to = Upload.random_file_name('classifieds/images'), blank = True)
    image_3 = models.ImageField(upload_to = Upload.random_file_name('classifieds/images'), blank = True)

    class Meta:
        verbose_name_plural = 'Classifieds'
        app_label = "main"
        db_table = "main_classifieds"

    def __unicode__(self):
        return self.title