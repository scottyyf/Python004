# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class SpidersPipeline:
    def process_item(self, item, spider):
        pds = pd.DataFrame(data=[[value for x, value in item.items()]])
        pds.to_csv('maoyan.csv', mode='a+', sep='#',
                   header=False, index=False, encoding='utf-8')

        return item
