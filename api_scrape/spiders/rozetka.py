import scrapy
import json


class RozetkaSpider(scrapy.Spider):
    name = "rozetka"
    allowed_domains = ["search.rozetka.com.ua"]
    search_text = "Радіо"

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://search.rozetka.com.ua/ua/search/api/v6/?front-type=xl&country=UA&page=1&text={self.search_text}",
            callback=self.parse_page)

    def parse_page(self, response):
        result = json.loads(response.body)
        goods = result.get("data").get("goods")

        for good in goods:
            yield {
                "title": good.get("title"),
                "link": good.get("href"),
                "price": good.get("price"),
                "status": good.get("status"),
                "stars": good.get("stars"),
            }

        page_num = result.get("data").get("pagination").get("shown_page")
        max_page = result.get("data").get("pagination").get("total_pages")

        if page_num != max_page:
            yield scrapy.Request(
                url=f"https://search.rozetka.com.ua/ua/search/api/v6/?front-type=xl&country=UA&page={page_num + 1}&text={self.search_text}",
                callback=self.parse_page)
