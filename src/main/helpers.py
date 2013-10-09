import os, re
from uuid import uuid4
from django.db.models import Q
from django.utils import encoding
from PIL import Image, ImageOps
from django.conf import settings

class Search:
    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    @staticmethod
    def get_query(query_string, search_fields):
        query = None
        terms = Search.normalize_query(query_string)
        for term in terms:
            or_query = None
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

class Seo:
    @staticmethod
    def prepareClassifiedUrl(classified, max_length = 32):
        title = re.sub('[^0-9a-zA-Z]+', ' ', classified.title).strip()
        url = "%s:%d" % (title[:max_length].lower().replace(' ', '-'), classified.id)
        return url

class Upload:
    @staticmethod
    def random_file_name(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            filename = '{}.{}'.format(uuid4().hex, ext)
            return os.path.join(path, filename)
        return wrapper

    @staticmethod
    def generate_thumb(imagepath, width, height, quality = 80):
        if not imagepath:
            return
        imagepath = str(imagepath)

        image = Image.open(os.path.join(settings.MEDIA_ROOT, imagepath))
        
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")
        ext = str(imagepath).split('.')[-1]
        ext = 'jpg'
        filename = str(imagepath).split('.')[0]
        
        filename = '{}.thumb.{}.{}'.format(filename, width, ext)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        imagefit = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        imagefit.save(filepath, 'JPEG', quality = quality)
        return filepath

    @staticmethod
    def generate_classified_thumbs(imagepath, quality = 80):
        if not imagepath:
            return
        for size in settings.CLASSIFIED_THUMBNAILS:
            print 'Generating thumbnail with size: %sx%s' % (size['width'], size['height'])
            Upload.generate_thumb(imagepath, size['width'], size['height'], quality)