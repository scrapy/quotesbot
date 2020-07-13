import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags > a.tag::text").getall()
            }

        next_page_url = response.css("li.next > a::attr(href)").get()
        if next_page_url is not None:
            yield response.follow(next_page_url)
