#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import scrapy
import re
from urlparse import urlparse
import json
import urllib2
import urllib
import StringIO

from geopy.geocoders import Nominatim

geolocator = Nominatim()


class DineSpider(scrapy.Spider):
    name = "badfood"

    def start_requests(self):
        urls = [
            #            'http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results',
            "http://www.foodauthority.nsw.gov.au/offences/prosecutions"
        ]
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
        date = response.xpath("//table//td/text()").extract()[7]
        finereason = response.xpath("//table//td/text()").extract()[8]
        latlong = decodeAddressToCoordinates(address)
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


def decodeAddressToCoordinates(address):
    urlParams = {"address": address, "sensor": "false"}
    url = "http://maps.google.com/maps/api/geocode/json?" + urllib.urlencode(urlParams)
    response = urllib2.urlopen(url)
    responseBody = response.read()

    body = StringIO.StringIO(responseBody)
    result = json.load(body)
    if "status" not in result or result["status"] != "OK":
        return None
    else:
        return (
            result["results"][0]["geometry"]["location"]["lat"],
            result["results"][0]["geometry"]["location"]["lng"],
        )
