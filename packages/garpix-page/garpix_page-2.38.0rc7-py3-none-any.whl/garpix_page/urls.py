from django.urls import path, re_path
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from garpix_page.views.clear_cache import clear_cache
from garpix_page.views.page_api import PageApiView, PageApiListView
from garpix_page.views.robots import robots_txt
from garpix_page.views.sitemap import sitemap_view
from garpix_page.views.get_template import GetTemplate
from garpix_page.views.upload import DgjsUpload

app_name = 'garpix_page'

urlpatterns = [
    path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
    path('dgjs_upload/', DgjsUpload.as_view(), name='dgjs_upload'),
    re_path(r'{}/page_models_list/$'.format(settings.API_URL), PageApiListView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)/$'.format(settings.API_URL), PageApiView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)$'.format(settings.API_URL), PageApiView.as_view()),
    path('sitemap.xml', sitemap, sitemap_view(), name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('admin/clear_cache', clear_cache, name='admin_clear_cache'),
]
