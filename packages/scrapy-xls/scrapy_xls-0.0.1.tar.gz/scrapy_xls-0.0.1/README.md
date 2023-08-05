# XLS Scrapy Spider 
Scrapy spider for parsing XLS files. It receives a XLS file in a response; iterates through each of its rows, and calls `parse_row` with a dict containing each field's data and the sheet name. Inspired in the builtin CSV feed scrapy spider.

This is built on top of openpyxl and pandas libs, you can set some options regarding the XLS file, such as the sheet names and number of rows to be skiped.
If sheets are not provided, it'll returns all sheets available.


## Installation

`pip install scrapy_xls`



## How to use

```
from scrapy_xls import XLSSpider


def SuperMarketCatalogSpider(XLSSpider):

    start_urls = [
        'https://www.supermarket.com/files/catalog-oct-22.xlsx',
        'https://www.supermarket.com/files/catalog-set-22.xlsx',
    ]

    skip_rows = 3 # Assuming that the sheet headers starts at the 4th row
    sheets = ['FRUITS', 'BEVERAGES']

    def parse_row(self, response, sheet, row):
        item = {}
        item['department'] = sheet
        item['product'] = row['NAME']
        item['price'] = row['PRICE']
        item['brand'] = row['BRAND']
        yield item

```


## Contributing

Feel free to contribute with the project. [Git repository](https://github.com/kennyaires/scrapy-xls).

<a href="https://www.buymeacoffee.com/kennyaires" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>