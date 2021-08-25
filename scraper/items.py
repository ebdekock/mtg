# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


def remove_fullstops(text):
    # strip the unicode quotes
    text = text.replace(".", "-")
    return text


# Output is a list by default, return the first item
class CardItem(Item):
    name = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    image_url = Field(output_processor=TakeFirst())
    store = Field(input_processor=MapCompose(remove_fullstops), output_processor=TakeFirst())
    search_id = Field(output_processor=TakeFirst())


class SearchItem(Item):
    search_term = Field(output_processor=TakeFirst())
    search_id = Field(output_processor=TakeFirst())
    datetime = Field(output_processor=TakeFirst())
