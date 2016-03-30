# -*- encoding: utf-8 -*-

import hashlib
import imghdr
import os
import sys

from bs4 import BeautifulSoup
from django.contrib.staticfiles.templatetags.staticfiles import static

if sys.version_info > (3, 0):
    from urllib.request import build_opener
else:
    from urllib2 import build_opener

from django import template
from django.conf import settings

register = template.Library()


def get_extensions():
    return ['jpg', 'jpeg', 'png', 'gif']


def _download(file_path, url):
    with open(file_path, 'wb') as fio:
        opener = build_opener()
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1')]
        fio.write(opener.open(url).read())
        fio.flush()

    extension = imghdr.what(file_path)
    if extension in get_extensions():
        old_file_path = file_path
        file_path = "%s.%s" % (file_path, extension)
        os.rename(old_file_path, file_path)
        for ext in get_extensions():
            sym_path = "%s.%s" % (old_file_path, ext)
            if ext != extension or not os.path.exists(sym_path):
                os.symlink(file_path, sym_path)
    return file_path


def get_filename(url):
    if sys.version_info > (3, 0):
        link = str(url).encode('utf-8')
    else:
        link = str(url)
    return hashlib.md5(link).hexdigest()


def get_folder(folder_type='img'):
    folder = os.path.join(settings.STATIC_ROOT, 'remdow/%s' % folder_type)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def download_link(value, type_link):
    m = get_filename(value)
    file_path = os.path.join(get_folder(type_link), m)

    if not os.path.exists(file_path + '.%s' % 'png'):
        file_path = _download(file_path, value)
        _, file_extension = os.path.splitext(file_path)
        if file_extension:
            result = static('remdow/%s/%s.%s' % (type_link, m, file_extension))
        else:
            result = static('remdow/%s/%s' % (type_link, m))
    else:
        result = static('remdow/%s/%s.%s' % (type_link, m, 'png'))
    return result


@register.filter
def remdow(value):
    soup = BeautifulSoup(value, "html.parser")
    links = soup.find_all('img', src=True)
    for link in links:
        link["src"] = download_link(link["src"], 'img')
    return str(soup)


@register.filter
def responsive(value):
    soup = BeautifulSoup(value, "html.parser")
    links = soup.find_all('img', src=True)
    for link in links:
        link["class"] = link.get('class', []) + ['img-responsive']
    return str(soup)
