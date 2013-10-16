# -*- coding: utf-8 -*-
import os, re
from uuid import uuid4
from django.db.models import Q
from django.utils import encoding
from PIL import Image, ImageOps
from django.conf import settings

class Search:
    @staticmethod
    def normalizeQuery(query_string, findterms = re.compile(r'"([^"]+)"|(\S+)').findall, normspace = re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    @staticmethod
    def prepareClassifiedQuery(request):
        print request.POST.get('price_min')
        print request.POST.get('price_max')
        print '------------------'
        return Search.buildQuery(
            request.POST.get('search'),
            ['title', 'content'],
            request.POST, 
            ['city_id', 'category', 'currency'],
            {
                'price': [request.POST.get('price_min'), request.POST.get('price_max')],
            }
        )

    @staticmethod
    def buildQuery(query_string, query_string_or_fields = [], extra_data = [], extra_data_and_fields = [], extra_data_and_between_fields = []):
        #TODO: Add filter by extra_data_and_between_fields in order to prepare the query to distinct between min/max price rate
        query = None
        terms = Search.normalizeQuery(query_string)
        for term in terms:
            or_query = None
            for field_name in query_string_or_fields:
                q = Q(**{'%s__icontains' % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query 
            else:
                query = query & or_query
        
        if extra_data:
            for extra in extra_data:
                if extra in extra_data_and_fields and extra_data[extra]:
                    q = Q(**{extra: extra_data[extra]})
                    if query is None:
                        query = q
                    else:
                        query = query & q

        #fix
        range = [u'', u'']
        for between_field in extra_data_and_between_fields:
            range = extra_data_and_between_fields[between_field]

        query = query & Q(**{'price__range': range})

        print '************************************************************************'
        print query
        print '************************************************************************'
        return query


    def appendQuery(originalQuery = None, appendQuery = None):
        if originalQuery is None:
            query = appendQuery 
        else:
            query = originalQuery & originalQuery
        return query

class Seo:
    @staticmethod
    def prepareClassifiedUrl(classified, max_length = 32):
        title = re.sub('[^0-9a-zA-Z]+', ' ', classified.title).strip()
        url = '%s:%d' % (title[:max_length].lower().replace(' ', '-'), classified.id)
        return url

class Upload:
    @staticmethod
    def generateRandomFilename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            filename = '{}.{}'.format(uuid4().hex, ext)
            return os.path.join(path, filename)
        return wrapper

    @staticmethod
    def generateThumbnail(imagepath, width, height, quality = 80):
        if not imagepath:
            return
        imagepath = str(imagepath)

        image = Image.open(os.path.join(settings.MEDIA_ROOT, imagepath))
        
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        ext = str(imagepath).split('.')[-1]
        ext = 'jpg'
        filename = str(imagepath).split('.')[0]
        
        filename = '{}.thumb.{}.{}'.format(filename, width, ext)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        imagefit = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        imagefit.save(filepath, 'JPEG', quality = quality)
        return filepath

    @staticmethod
    def generateClassifiedThumbs(imagepath, quality = 80):
        if not imagepath:
            return
        for size in settings.CLASSIFIED_THUMBNAILS:
            print 'Generating thumbnail for \'%s\' with size: %sx%s' % (imagepath, size['width'], size['height'])
            Upload.generateThumbnail(imagepath, size['width'], size['height'], quality)

    @staticmethod
    def generateClassifiedThumbsByRequest(request, classified, names = ['image_1', 'image_2', 'image_3']):
        for name in names:
            if request.FILES.get(name):
                Upload.generateClassifiedThumbs(getattr(classified, name))