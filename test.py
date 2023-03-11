from scrapy.http import Request
from urllib import parse


print(parse.urljoin('https://www.v2ph.com/album/am4m5e8z.html?page=2', '/album/am4m5e8z.html?page=3'))