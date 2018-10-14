#!/usr/bin/env python3

from urllib.request import urlopen
import geodecode
import json
import re
import scrapy
import urllib.parse

from geopy.geocoders import Nominatim

geolocator = Nominatim()


class Spider(scrapy.Spider):
    name = "badfood"

    def start_requests(self):
        urls = ["http://www.foodauthority.nsw.gov.au/offences/prosecutions"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css("table").xpath("//@href").extract()
        paths = []

        for i in range(0, len(hrefs)):
            if re.search("offences\/prosecutions\/", hrefs[i]):
                print(hrefs[i])
                paths.append(hrefs[i])

        for i in range(0, len(paths)):
            yield scrapy.Request(
                "http://www.foodauthority.nsw.gov.au" + paths[i], callback=self.parse2
            )

    def parse2(self, response):
        name = response.xpath("//table//td/text()").extract()[0]
        address = "".join(response.xpath("//table//p/text()").extract()[1:4])
        print(address)
        date = response.xpath("//table//td/text()").extract()[7]
        finereason = response.xpath("//table//td/text()").extract()[8]
        latlong = geodecode.decodeAddressToCoordinates(address)
        if latlong is None:
            latlong = "Not Found"
        yield {
            "name": name,
            "address": address,
            "date": date,
            "url": response.url,
            "latlong": latlong,
            "finereason": finereason,
        }
