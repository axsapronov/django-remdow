# -*- encoding: utf-8 -*-

import hashlib
import os
import sys

from django.contrib.staticfiles.templatetags.staticfiles import static

if sys.version_info > (3, 0):
    from urllib.request import build_opener
else:
    from urllib2 import build_opener

from django import template
from django.conf import settings

register = template.Library()


def download_image(file_path, url):
    with open(file_path, 'wb') as fio:
        opener = build_opener()
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1')]
        fio.write(opener.open(url).read())
        fio.flush()
    return True


@register.filter
def download(value):
    if sys.version_info > (3, 0):
        link = str(value).encode('utf-8')
    else:
        link = str(value)
    m = hashlib.md5(link).hexdigest()

    folder = os.path.join(settings.STATIC_ROOT, 'remdow')
    if not os.path.isdir(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, m)

    if os.path.exists(file_path) or download_image(file_path, value):
        result = static('remdow/%s' % m)
    else:
        result = value
    return result
