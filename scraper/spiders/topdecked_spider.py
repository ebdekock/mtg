from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from items import CardItem, SearchItem


class TopDeckedSpider(scrapy.Spider):
    name = "topdecked"

    def start_requests(self):
        yield SplashRequest(
            f"https://store.topdecksa.co.za/pages/search-results-page?q={self.search_term}&rb_product_type=Singles",
            self.parse,
            args={"wait": 1},
        )

    def parse(self, response):
        # Get vars
        print("Start TopDecked spider parse")
        top_results = response.css(".snize-search-results-content li")
        store = "SATopDecked"
        now = datetime.utcnow()
        search_id = self.uuid

        # Populate SearchItem
        search_loader = ItemLoader(item=SearchItem())
        search_loader.add_value("search_term", self.search_term)
        search_loader.add_value("search_id", search_id)
        search_loader.add_value("datetime", now)
        yield search_loader.load_item()

        # If the list of no products and suggestions is displayed, there are no results,
        # it will list alternatives that we don't currently care about
        no_results = response.css("li.snize-no-products-found.snize-with-suggestion")

        # Populate results
        if not no_results:
            for result in top_results:
                prices = result.css("span.snize-price::text")
                print(prices[0].extract())
                price = int(prices[0].extract().strip().replace("R ", "").split(".")[0])

                loader = ItemLoader(item=CardItem(), selector=result)
                loader.add_value("store", store)
                loader.add_value("search_id", search_id)
                loader.add_css("name", "span.snize-title::text")
                loader.add_value("price", price)
                loader.add_css("image_url", "img.snize-item-image::attr(src)")
                yield loader.load_item()
