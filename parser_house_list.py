# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import traceback

import requests
from bs4 import BeautifulSoup

from utils import delete_table_space_enter, BASE_URL

TOWN_URL_TEMPLATE = BASE_URL + '%s/rs'
PAGE_URL_TEMPLATE = BASE_URL + '%s/d%srs'


def parser_house(district):
    town_url = TOWN_URL_TEMPLATE % district
    count = 0
    try:
        base_html = requests.get(town_url)
        base_bs = BeautifulSoup(base_html.text, "lxml")

        print "=====pages====="
        page_div = base_bs.find('div', attrs={"class": "page-box house-lst-page-box"})
        # total_page_a = page_div.find('a', attrs={"gahref": "results_totalpage"})
        # page_numbs = int(total_page_a.get_text())
        if not page_div:
            return count
        page_as = page_div.find_all('a')
        if len(page_as) == 1:
            page_numbs = 1
        else:
            page_numbs = int(delete_table_space_enter(page_as[-2].get_text()))
        print "总页数：", page_numbs
        with open('house_data.txt', 'a') as fp:
            for i in xrange(page_numbs):
                print "=============>page %d<=============" % (i+1)
                content = requests.get(PAGE_URL_TEMPLATE % (district, i+1))
                content_bs = BeautifulSoup(content.text, "lxml")
                house_lst = content_bs.find(id="house-lst")
                all_lis = house_lst.find_all('li')
                for li in all_lis:
                    count += 1
                    h2 = li.find('h2')
                    title = h2.a['title']

                    where = li.find('div', attrs={"class": "where"})
                    community = where.a.span['title']
                    spans = where.find_all('span', recursive=False)
                    rooms = delete_table_space_enter(spans[0].text)
                    area = delete_table_space_enter(spans[1].string)
                    other = li.find('div', attrs={"class": "other"})
                    age_str = other.find('div').get_text().split('|')
                    if len(age_str) == 4:
                        age = delete_table_space_enter(age_str[3])
                        age = int(age[0:4])
                    else:
                        age = 0
                    price_bs = li.find('div', attrs={"class": "price"})
                    price = delete_table_space_enter(price_bs.span.string)

                    price_pre = delete_table_space_enter(li.find('div', attrs={"class": "price-pre"}).get_text())
                    print '===>%s<===' % title
                    print community, rooms, area, age, price, price_pre
                    fp.write(str("%s %s %s %s %s %s %s\n" % (title, community, rooms, area, age, price, price_pre)).encode('utf8'))

        print "=" * 50
        print "房源总数：%d" % count
        print "=" * 50
    except Exception, e:
        traceback.print_exc()
    return count

if __name__ == '__main__':
    parser_house('datuanzhen')

