from pathlib import Path

import scrapy


# run with:
# scrapy crawl quote -O quotes.json

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # can use start_urls to use default start_requests implementation
    # start_urls = [
    #         'https://quotes.toscrape.com/page/1/',
    #         'https://quotes.toscrape.com/page/2/',
    #     ]

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # following links to load more pages
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # shortcut for creating Request objects:
            yield response.follow(next_page, callback=self.parse)
            
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)