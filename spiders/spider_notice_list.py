#!/usr/bin/env python3

import geodecode
import re
import scrapy
import urllib.parse


class Spider(scrapy.Spider):
    name = "badfood"

    def start_requests(self):
        urls = [
            "http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css("table").xpath("//@href").extract()
        paths = []

        for i in range(0, len(hrefs)):
            if len(urllib.parse.urlparse(hrefs[i]).query) > 0 and re.search(
                "itemId", urllib.parse.urlparse(hrefs[i]).query
            ):
                paths.append(urllib.parse.urlparse(hrefs[i]).query)
        for i in range(0, len(paths)):
            yield scrapy.Request(
                "http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?"
                + paths[i],
                callback=self.parse2,
            )

    def parse2(self, response):
        name = response.xpath("//table//td/text()").extract()[1]
        address = response.xpath("//table//td/text()").extract()[3]
        suburb = response.xpath("//table//td/text()").extract()[4]
        date = response.xpath("//table//td/text()").extract()[6]
        finereason = response.xpath("//table//td/text()").extract()[8]
        latlong = geodecode.decodeAddressToCoordinates(address + suburb)
        if latlong is None:
            latlong = "Not Found"
        yield {
            "name": name,
            "address": address + suburb,
            "date": date,
            "url": response.url,
            "latlong": latlong,
            "finereason": finereason,
        }
