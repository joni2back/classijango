# -*- coding: utf-8 -*-
import os, re, sys, logging
from uuid import uuid4
from django.db.models import Q
from django.utils import encoding
from PIL import Image, ImageOps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class Search:

    @staticmethod
    def urlFromString(string, max_length = 45):
        string = re.sub('[^0-9a-zA-Z]+', ' ', string).strip()
        return string[:max_length].lower().replace(' ', '-')

    @staticmethod
    def normalizeQuery(query_string, findterms = re.compile(r'"([^"]+)"|(\S+)').findall, normspace = re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    @staticmethod
    def prepareClassifiedQuery(request):
        return Search.buildQuery(
            request.GET.get('search'),
            ['title', 'content'],
            request.GET, 
            ['city_id', 'category', 'currency'],
            {
                'price': [
                    request.GET.get('price_min'), 
                    request.GET.get('price_max')
                ],
            }
        )

    @staticmethod
    def buildQuery(query_string = '', query_string_or_fields = [], extra_data = [], extra_data_and_fields = [], extra_data_and_between_fields = []):
        query = Q(**{})
        if query_string:
            terms = Search.normalizeQuery(query_string)
            for term in terms:
                or_query = Q(**{})
                for field_name in query_string_or_fields:
                    q = Q(**{'%s__icontains' % field_name: term})
                    query = Search.appendQuery(query, q, True)
        if extra_data:
            for extra in extra_data:
                if extra in extra_data_and_fields and extra_data[extra]:
                    q = Q(**{extra: extra_data[extra]})
                    query = Search.appendQuery(query, q)      
        for between_field in extra_data_and_between_fields:
            min_max = extra_data_and_between_fields[between_field]
            if any(min_max):
                if not min_max[0]:
                    min_max[0] = 0
                if not min_max[1]:
                    min_max[1] = sys.maxint
                q = Q(**{'%s__range' % between_field: (Search.intForceCast(min_max[0]), Search.intForceCast(min_max[1]))})
                query = Search.appendQuery(query, q)
        Logger.getInstance().debug(query)
        return query

    @staticmethod
    def appendQuery(original_query = None, append_query = None, append_as_or = False):
        if original_query == Q(**{}):
            query = append_query 
        else:
            if append_as_or:
                query = original_query | append_query
            else:
                query = original_query & append_query
        return query
    
    @staticmethod
    def intForceCast(var):
        try:
            return int(var)
        except:
            return 0

class Upload:
    @staticmethod
    def generateRandomFilename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            filename = '{}.{}'.format(uuid4().hex, ext)
            return os.path.join(path, filename)
        return wrapper

    @staticmethod
    def generateThumbnail(imagepath, postfix, width, height, quality = 80):
        if not imagepath:
            return
        imagepath = str(imagepath)

        image = Image.open(os.path.join(settings.MEDIA_ROOT, imagepath))
        
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        filename = str(imagepath).split('.')[0]
        filename = Upload.getThumbFilename(filename, postfix)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        imagefit = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        imagefit.save(filepath, settings.CLASSIFIED_THUMBNAILS_CONVERSION_TYPE, quality = quality)
        return filepath

    @staticmethod
    def generateClassifiedThumbs(imagepath):
        if not imagepath:
            return
        for size in settings.CLASSIFIED_THUMBNAILS:
            width = settings.CLASSIFIED_THUMBNAILS[size]['width']
            height = settings.CLASSIFIED_THUMBNAILS[size]['height']
            quality = settings.CLASSIFIED_THUMBNAILS[size]['quality']
            Logger.getInstance().debug('Generating thumbnail for \'%s\' (%s) with size: %sx%s with quality %s%%' % (imagepath, size, width, height, quality))
            Upload.generateThumbnail(imagepath, size, width, height, quality)

    @staticmethod
    def getClasifiedThumbs(filename):
        thumbs = {}
        if not filename:
            return
        for size in settings.CLASSIFIED_THUMBNAILS:
            width = settings.CLASSIFIED_THUMBNAILS[size]['width']
            height = settings.CLASSIFIED_THUMBNAILS[size]['height']
            quality = settings.CLASSIFIED_THUMBNAILS[size]['quality']
            thumbs[size] = Upload.getThumbFilename(filename, size)
        return thumbs

    @staticmethod
    def generateClassifiedThumbsByRequest(request, classified, names = ['image_1', 'image_2', 'image_3']):
        for name in names:
            if request.FILES.get(name):
                Upload.generateClassifiedThumbs(getattr(classified, name))

    @staticmethod
    def getThumbFilename(imagepath, postfix):
        filename = str(imagepath).split('.')[0]
        return '{}.{}.{}'.format(filename, postfix, settings.CLASSIFIED_THUMBNAILS_EXT)

class Email:
    @staticmethod
    def sendClassifiedCreationEmail(classified):
        subject, from_email, to = classified.title, settings.DEFAULT_FROM_EMAIL, classified.contact_email
        text_content = classified.content
        html_content = classified.content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if str(classified.image_1):
            img = os.path.join(settings.MEDIA_ROOT, str(classified.image_1))
            msg.attach_file(img)

        return msg.send()

class Logger:
    @staticmethod
    def getInstance(logger_name = 'classijango'):
        return logging.getLogger(logger_name)