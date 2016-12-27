# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import traceback

import requests
from bs4 import BeautifulSoup

from utils import BASE_URL


def parser_district(url):
    try:
        base_html = requests.get(url)
        base_bs = BeautifulSoup(base_html.text, "lxml")

        district_div = base_bs.find('div', attrs={"class": "option-list gio_district"})
        district_as = district_div.find_all('a')[1:-1]
        district_list = [one['gahref'] for one in district_as]
        return district_list
    except Exception:
        traceback.print_exc()
        return []


def parser_town(town='pudongxinqu'):
    town_list = []
    try:
        base_html = requests.get(BASE_URL+town+'/rs')
        base_bs = BeautifulSoup(base_html.text, 'lxml')

        town_div = base_bs.find('div', attrs={'class': 'option-list sub-option-list gio_plate'})
        town_as = town_div.find_all('a')[1:]
        town_list = [one['gahref'] for one in town_as]
        print "=" * 20, ">%s所有城镇<" % town, "=" * 20
        print town_list
        print "=" * 50
        return town_list
    except Exception:
        traceback.print_exc()
        return town_list

if __name__ == "__main__":
    # parser_district(BASE_URL)
    parser_town()
