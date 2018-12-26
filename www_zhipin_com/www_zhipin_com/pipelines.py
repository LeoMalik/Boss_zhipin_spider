# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    def __init__(self):
        self.jid_set = set()

    def process_item(self, item, spider):
        pid = item['pid']
        if pid in self.jid_set:
            raise DropItem("Duplicate job found:%s" % item)

        self.jid_set.add(pid)
        return item
