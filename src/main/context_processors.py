# -*- coding: utf-8 -*-
from main.models.categories import ClassifiedCategory
from main.models.classifieds import Classified

# We are saving in session as cache until the implementation of real cache such as memcached

def trendingCategories(request):
    if not request.session.get('categories'):
        request.session['categories'] = ClassifiedCategory.objects.all()[:5]
    return {
        'trendingCategories': request.session.get('categories')
    }

def latestClassifieds(request):
    if not request.session.get('latest_classifieds'):
        request.session['latest_classifieds'] = Classified.objects.all().order_by('pk')[:5]
    return {
        'latestClassifieds': request.session.get('latest_classifieds')
    }

