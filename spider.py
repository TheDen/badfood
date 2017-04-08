#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import scrapy
import re
from urlparse import urlparse
import json

from geopy.geocoders import Nominatim
geolocator = Nominatim()

class DineSpider(scrapy.Spider):
    name = "badfood"

    def start_requests(self):
        urls = [
            'http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('table').xpath('//@href').extract()

        paths = []
        for i in range(0, len(hrefs)):
          if len(urlparse(hrefs[i]).query) > 0 and re.search('itemId',urlparse(hrefs[i]).query) :
           paths.append(urlparse(hrefs[i]).query)        
        
        for i in range(0, len(paths)):
            yield scrapy.Request('http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?'+ paths[i], callback=self.parse2)
 
    def parse2(self, response): 
       name = response.xpath("//table//td/text()").extract()[1]
       address = response.xpath("//table//td/text()").extract()[3]
       suburb = response.xpath("//table//td/text()").extract()[4]
       date = response.xpath("//table//td/text()").extract()[6]
       location = geolocator.geocode(address)
       if location:
        latlong = location.latitude,location.longitude
       else:
        latlong = "not found"
       yield {
                'name': name,
                'address': address+suburb,
                'date': date, 
                'url': response.url,
                'latlong': latlong
        } 
