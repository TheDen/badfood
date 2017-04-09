# [BadFood.io]((badfood.io))


Shows a map of restaurants in Sydney that have been given a penalty from [The Department of Primary Industries Food Authority](http://www.foodauthority.nsw.gov.au/), specifically from [this](http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results) public penalty notice list.

Data is scraped using a spider with python's `scrapy` and stored in a remote mongodb and served as a NodeJs+Express+EJS on Heroku.

## Build

Python's scrapy: `pip install scrapy`

Node: `nvm install && npm install`

## Run

Crawl the data and output it as JSON, run the spider:
```scrapy runspider spider.py -o output.json```

Import the data to a remote host:

```
mongoimport -h mongohost -d dbname -c collection -u username -p password --file output.json --jsonArray
```

Export the google maps API URL (Including the key) as an environment variable (or as a config var on Heroku):

`export APIKEY="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=initMap"`

and similarly the mongodb url, for example with `mlab`:

```export MONGOURL=mongodb://username:password@12345.mlab.com:55491/db```


## Contribute

* Pull requests are accepted.
* Thanks to [Deedee lee](http://github.com/deedeedeeps) for the BadFood emoji logo






