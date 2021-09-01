import re
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from items import CardItem, SearchItem


class BattleWizards(scrapy.Spider):
    name = "battlewizards"

    def start_requests(self):
        url = f"https://www.battlewizards.co.za/search.php?mode=1&search_query_adv={self.search_term}&brand=&searchsubs=ON&price_from=&price_to=&featured=&shipping=&category%5B%5D=18&section=product"

        # We need to scroll to the bottom of the page to ensure lazy loaded images load correctly
        scroll_script = f"""
        function main(splash)
            splash:go{{ "{url}", headers={{["content-type"]="application/json"}} }}
            splash:wait(1.0)
            splash:set_viewport_full()

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {{return document.body.scrollHeight;}}"
            )
            scroll_to(0, get_body_height())
            splash:wait(1.0)

            return splash:html()
        end
        """

        yield SplashRequest(
            url,
            self.parse,
            args={
                "lua_source": scroll_script,
            },
            endpoint="execute",
        )

    def parse(self, response):
        # Get vars
        print("Start BattleWizards spider parse")
        top_results = response.css("ul.productGrid > li")
        store = "BattleWizards"
        now = datetime.utcnow()
        search_id = self.uuid

        # Populate SearchItem
        search_loader = ItemLoader(item=SearchItem())
        search_loader.add_value("search_term", self.search_term)
        search_loader.add_value("search_id", search_id)
        search_loader.add_value("datetime", now)
        yield search_loader.load_item()

        for result in top_results:
            try:
                price = int(
                    result.css("span.price.price--withTax::text")
                    .extract_first()
                    .replace("R", "")
                    .split(".")[0]
                )
            except:  # noqa
                price = "Varies"

            loader = ItemLoader(item=CardItem(), selector=result)
            loader.add_value("store", store)
            loader.add_value("search_id", search_id)
            loader.add_css("name", "h4.card-title > a::text")
            loader.add_value("price", price)
            loader.add_css("image_url", "div.card-img-container > img::attr(src)")
            yield loader.load_item()
