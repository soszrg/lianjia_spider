# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

BASE_URL = u'http://sh.lianjia.com/ershoufang/'


def delete_table_space_enter(raw):
    return raw.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "").replace(' ', '')
