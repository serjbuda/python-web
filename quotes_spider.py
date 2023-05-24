import scrapy

class ToscrapeItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    author_info = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = ToscrapeItem()
            item['quote'] = quote.css('span.text::text').get()
            item['author'] = quote.css('span small::text').get()
            author_page_link = quote.css('span a::attr(href)').get()
            if author_page_link is not None:
                yield response.follow(author_page_link, self.parse_author, meta={'item': item})
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        item = response.meta['item']
        item['author_info'] = response.css('div.author-description::text').get()
        yield item
