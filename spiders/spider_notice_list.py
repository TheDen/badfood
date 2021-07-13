#!/usr/bin/env python3

import geodecode
import re
import scrapy
import urllib.parse


class Spider(scrapy.Spider):
    name = "badfood"

    def start_requests(self):
        urls = []
        for page in range(1, 13):
            urls.append(
                "https://www.foodauthority.nsw.gov.au/offences/penalty-notices?s=&page={}".format(
                    page
                )
            )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css("table").xpath("//@href").extract()
        paths = []

        for i in range(0, len(hrefs)):
            if re.search("/offences/penalty-notices/", hrefs[i]):
                paths.append(hrefs[i])
        for i in range(0, len(paths)):
            yield scrapy.Request(
                # "http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?"
                "https://www.foodauthority.nsw.gov.au" + paths[i],
                callback=self.parse2,
            )

    def parse2(self, response):
        name = (
            response.css(".field--name-field-penalty-notice-trade")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        address = (
            response.css(".field--name-field-penalty-notice-street")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        city = (
            response.css(".field--name-field-penalty-notice-city")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        zip = (
            response.css(".field--name-field-penalty-notice-zip")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        council = (
            response.css(".field--name-field-penalty-notice-council")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        date = (
            response.css(".field--name-field-penalty-notice-date")
            .css(".field__item")
            .xpath("./time/@datetime")
            .extract()[0]
        )
        finereason = (
            response.css(".field--name-field-penalty-notice-nature")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        penalty_amount = (
            response.css(".field--name-field-penalty-notice-amount")
            .css(".field__item")
            .xpath("./text()")
            .extract()[0]
        )
        latlong = geodecode.decodeAddressToCoordinates(
            address + council + city + zip,
        )
        if latlong is None:
            latlong = "Not Found"
        yield {
            "name": name,
            "address": address + council + city + zip,
            "penalty_amount": penalty_amount,
            "date": date,
            "url": response.url,
            "latlong": latlong,
            "finereason": finereason,
        }
