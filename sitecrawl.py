# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import gzip
from StringIO import StringIO


def crawler():
    count=0
    url="https://www.jobstreet.com.my/sitemap.htm"
    old_xml=requests.get(url)
    new_xml=gzip.GzipFile(fileobj=StringIO(old_xml.content)).read()
    final_xml=BeautifulSoup(new_xml)
    item_to_be_found=final_xml.findAll('loc')
    for i in item_to_be_found:
        count=count+1
        print i
        print count
    crawler()
