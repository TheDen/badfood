<div align="center">

[![BadFood](images/badfood.png)](https://badfood.theden.sh)

[![Code Style](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/TheDen/badfood/issues)
[![License](https://img.shields.io/github/license/theden/badfood?style=flat-square)](/LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)
![Github Pages](https://img.shields.io/badge/GitHub%20Pages-%23222222?style=flat-square&logo=github&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-%23E34F26?style=flat-square&logo=html5&logoColor=white)
![Javascript](https://img.shields.io/badge/javascript-%23F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-%231572B6?style=flat-square&logo=CSS3&logoColor=white)
[![Prettier](https://img.shields.io/badge/Prettier-%23F7B93E.svg?style=flat-square&logo=prettier&logoColor=black)](https://github.com/prettier/prettier)
[![Website Status](https://img.shields.io/website?label=badfood.theden.sh&style=flat-square&url=https%3A%2F%2Fbadfood.theden.sh%2F)](https://badfood.theden.sh/)

</div>

[BadFood](http://badfood.theden.sh) shows a map of restaurants in Sydney that have been given a penalty from [The Department of Primary Industries Food Authority](http://www.foodauthority.nsw.gov.au/), specifically from the public [penalty notice](http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results) and [prosecutions](http://www.foodauthority.nsw.gov.au/offences/prosecutions) lists.

## Building

### Data Crawler

Install the python3 requirements

```bash
pip install -r requirements.txt
```

## Running

### Data Crawling

To crawl the data from the notice list webpage, and store in in JSON format

```bash
GOOGLE_API_KEY="<YOUR_API_KEY>" scrapy runspider spiders/spider_notice_list.py -s USER_AGENT='Mozilla/5.0' -o notice_list.json
```

For the prosecutions list

```bash
GOOGLE_API_KEY="<YOUR_API_KEY>" scrapy runspider spiders/spider_prosecutions_list.py -s USER_AGENT='Mozilla/5.0' -o prosecutions_list.json
```

## Contributing

- Issues and pull requests are welcome
- Thanks to [Deedee lee](http://github.com/deedeedeeps) for the BadFood emoji logo
