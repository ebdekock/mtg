import re
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from items import CardItem, SearchItem


def get_price(text):
    price = re.search("- R (.+?)\.", text)  # noqa
    if price:
        return price.group(1)
    return "Varies"


class D20BattleGround(scrapy.Spider):
    name = "d20battleground"

    def start_requests(self):
        yield SplashRequest(
            f"https://d20battleground-za.myshopify.com/search?q=*{self.search_term}*+product_type%3A%22mtg%22",
            self.parse,
            args={"wait": 1},
        )

    def parse(self, response):
        # Get vars
        print("Start D20Battleground spider parse")
        top_results = response.css("div.row > div.col-md-4")
        store = "D20 Battleground"
        now = datetime.utcnow()
        search_id = self.uuid

        # Populate SearchItem
        search_loader = ItemLoader(item=SearchItem())
        search_loader.add_value("search_term", self.search_term)
        search_loader.add_value("search_id", search_id)
        search_loader.add_value("datetime", now)
        yield search_loader.load_item()

        for result in top_results:
            # See if theres stock
            stock = result.css("p.productPrice::text").extract_first()
            if "Sold Out" in stock:
                return

            # Get cheapest version available
            prices = result.css("div.addNow.single > p")
            try:
                price = min(
                    [
                        int(get_price(price.extract()))
                        for price in prices
                        if get_price(price.extract()) != "Varies"
                    ]
                )
            except:  # noqa
                price = "Varies"

            loader = ItemLoader(item=CardItem(), selector=result)
            loader.add_value("store", store)
            loader.add_value("search_id", search_id)
            loader.add_css("name", "p.productTitle::text")
            loader.add_value("price", price)
            loader.add_css("image_url", "img.items-even::attr(src)")
            yield loader.load_item()
