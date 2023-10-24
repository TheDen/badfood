#!/usr/bin/env python3

import os
from geopy.geocoders import Nominatim

import urllib.parse
from urllib.request import urlopen
import json


def decodeAddressToCoordinates(address):
    if "GOOGLE_API_KEY" in os.environ:
        google_token = os.environ.get("GOOGLE_API_KEY")

    url_params = {"address": address, "sensor": "false"}
    url = (
        "https://maps.google.com/maps/api/geocode/json?"
        + urllib.parse.urlencode(url_params)
        + "&key="
        + google_token
    )
    response = urlopen(url)
    response_body = response.read()
    result = json.loads(response_body)

    if "status" not in result or result["status"] != "OK":
        return None
    else:
        return (
            result["results"][0]["geometry"]["location"]["lat"],
            result["results"][0]["geometry"]["location"]["lng"],
        )
