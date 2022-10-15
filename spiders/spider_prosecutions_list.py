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
        urls = ["https://www.foodauthority.nsw.gov.au/offences/prosecutions"]
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
        name = (
            response.css(".field--name-field-prosecution-notice-trade")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        address = (
            response.css(".field--name-field-prosecution-notice-place")
            .css(".field__item")
            .css(".field__item")
            .xpath("./p")
            .xpath("./text()")
            .extract()
        )
        council = (
            response.css(".field--name-field-prosecution-notice-council")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        date = (
            response.css(".field--name-field-prosecution-notice-date")
            .css(".field__item")
            .xpath("./time/@datetime")
            .extract()[0]
        )
        finereason = "".join(
            response.css(".field--name-field-prosecution-notice-nature")
            .css(".field__item")
            .xpath(".//text()")
            .extract()
        )
        prosecution_amount = "".join(
            response.css(".field--name-field-prosecution-notice-penalty")
            .css(".field__item")
            .xpath(".//p")
            .xpath("./text()")
            .extract()
        )
        latlong = geodecode.decodeAddressToCoordinates(address)
        if latlong is None:
            latlong = "Not Found"
        yield {
            "name": name,
            "address": address,
            "penalty_amount": prosecution_amount,
            "date": date,
            "url": response.url,
            "latlong": latlong,
            "finereason": finereason,
        }
