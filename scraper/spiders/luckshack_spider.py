from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from items import CardItem, SearchItem


class LuckShackSpider(scrapy.Spider):
    name = "luckshack"

    def start_requests(self):
        yield SplashRequest(
            f"https://luckshack.co.za/index.php?route=product/asearch&search={self.search_term}",
            self.parse,
            args={"wait": 1},
        )

    def parse(self, response):
        # Get vars
        print("Start LuckShack spider parse")
        top_results = response.css("div.product-layout.product-list.col-xs-12")
        store = "Luckshack"
        now = datetime.utcnow()
        search_id = self.uuid

        # Populate SearchItem
        search_loader = ItemLoader(item=SearchItem())
        search_loader.add_value("search_term", self.search_term)
        search_loader.add_value("search_id", search_id)
        search_loader.add_value("datetime", now)
        yield search_loader.load_item()

        # If there are no results, a paragraph in this div will be displayed instead of results
        no_results = response.css("div#content > p::text")

        # Populate results
        if not no_results:
            for result in top_results:

                # Try get lowest price, otherwise just use first
                prices = result.css("table.table.table-striped h5 > b::text")
                try:
                    # If theres no price, it could mean the cards discounted, look for the new price
                    if not prices[0].extract().strip():
                        prices = result.css("table.table.table-striped h5 > b > span.price-new::text")
                    lowest_price = int(
                        min([float(price.extract().strip().replace("R", "")) for price in prices])
                    )
                except:  # noqa
                    lowest_price = int(prices[0].extract().strip().replace("R", "").split(".")[0])

                loader = ItemLoader(item=CardItem(), selector=result)
                loader.add_value("store", store)
                loader.add_value("search_id", search_id)
                loader.add_css("name", "div.product-thumb > div.caption > h4 > a::text")
                loader.add_value("price", lowest_price)
                loader.add_css("image_url", "div.image > a > img::attr(src)")
                yield loader.load_item()
