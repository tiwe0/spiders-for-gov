from typing import Any, Generator, Iterable, List, Optional, Union

from search_engine.basepro import ZhengFuBaseSpider
from scrapy.responsetypes import Response
from scrapy import Selector


class A太原Spider(ZhengFuBaseSpider):
    """POST
    TODO token 反爬"""
    custom_settings: Optional[dict] = {
        'DOWNLOADER_MIDDLEWARES': {
            'search_engine.middlewares.WordTokenDownloaderMiddleware': 543,
        },
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.5,
    }
    name: str = '太原'
    token_url = 'http://www.taiyuan.gov.cn/so/s?tab=all&siteCode=1401000055&qt={keyword}'
    api = 'https://api.so-gov.cn/s'
    method = "POST"
    debug: bool = False
    data = {
        "siteCode": "1401000055",
        "tab": "all",
        "timestamp": "{timestamp}",
        "wordToken": "{wordtoken}",
        "page": "{page}",
        "pageSize": "20",
        "qt": "{keyword}",
        "timeOption": "0",
        "sort": "relevance",
        "keyPlace": "0",
        "fileType": "",
    }

    def edit_page(self, response):
        # inspect_response(response, self)
        raw_data = response.json()
        total_items_num = raw_data["data"]["search"]["totalHits"]
        total_page = int(total_items_num) // 20 + 1
        return total_page

    def edit_items_box(self, response):
        raw_data = response.json()
        items_box = raw_data["data"]["search"]["searchs"]
        return items_box

    def edit_item(self, item: Any) -> Optional[dict[str, Union[str, int]]]:
        result = {
            "title": item.get("title", ""),
            "url": item.get("viewUrl", ""),
            "date": item.get("docDate", ""),
            "source": item.get("siteName", ""),
            "type": item.get("displayDb", ""),
        }
        return result

