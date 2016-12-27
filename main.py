# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from parser_district_town import parser_district, parser_town
from parser_house_list import parser_house
from utils import BASE_URL

if __name__ == '__main__':
    total_house = 0
    district_list = None
    town_dict = None
    district_list = parser_district(BASE_URL)
    print "=" * 30, ">上海所有行政区<", "=" * 30
    print district_list
    print "=" * 70
    town_dict = {one: parser_town(one) for one in district_list}
    print town_dict

    def count(town):
        global total_house
        new_house = parser_house(town)
        total_house += new_house
        return new_house
    town_hours_count = {y: count(y) for x in town_dict for y in town_dict[x]}
    print town_hours_count

    print "=" * 50
    print "房源总数：%d" % total_house
    print "=" * 50
