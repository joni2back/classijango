import os, re
from uuid import uuid4
from django.db.models import Q
from django.utils import encoding

def ucwords(string):
    return " ".join([w[0].upper() + w[1:] for w in re.split('\s*', string.lower())])

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