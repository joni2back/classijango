from django.db import models
from main.models.categories import ClassifiedCategory
from main.models.status import ClassifiedStatus
from django.contrib.auth.models import User
import datetime, calendar, Image

CLASSIFIED_EXPIRATION_MONTHS = 9999

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

class Classified(models.Model):

    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)

    expirationDate = add_months(datetime.date.today(), CLASSIFIED_EXPIRATION_MONTHS)

    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True)
    category = models.ForeignKey(ClassifiedCategory)
    status = models.SmallIntegerField(max_length=1, choices=CLASSIFIED_STATUS, default=1)
    type = models.CharField(max_length=12, choices=CLASSIFIED_TYPES, default='sale')
    currency = models.CharField(max_length=12, choices=CLASSIFIED_CURRENCIES, default='peso_arg')
    created = models.DateTimeField(auto_now=True)
    expires = models.DateField(default=expirationDate)
    price = models.FloatField(null=True)
    phone = models.CharField(max_length=32, null=True)
    google_map = models.CharField(max_length=128, null=True)

    image_1 = models.ImageField(upload_to='images', blank=True)
    image_3 = models.ImageField(upload_to='images', blank=True)
    image_2 = models.ImageField(upload_to='images', blank=True)




    class Meta:
        verbose_name_plural = 'Classifieds'
        app_label = "main"
        db_table = "main_classifieds"

    def __unicode__(self):
        return self.title