# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuctionresultsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    property_id = scrapy.Field()
    property_address = scrapy.Field()
    property_region_district = scrapy.Field()
    property_beds = scrapy.Field()
    property_baths = scrapy.Field()
    property_carparks = scrapy.Field()
    property_area = scrapy.Field()
    property_value = scrapy.Field()
    property_auctiondetails = scrapy.Field()
    property_ratingvalue = scrapy.Field()
    property_agentdetails = scrapy.Field()
    property_auction_status = scrapy.Field()
    pass
