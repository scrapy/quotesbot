# import sys
# print(sys.version)
# 路徑：C:\user\Anaconda3\envs\scrapyTest\Lib\site-packages\scrapy\booksDemo
import sys
import io
import scrapy
from urllib import parse as urlparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class booksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.com.tw"]
    start_urls = [
        "http://activity.books.com.tw/everylettermatters/sentence/latest"
    ]

    # def parse(self, response):
    #     filename = response.url.split("/")[-2]
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)

    def parse(self, response):
        # learn_nodes = response.css('div.item')
        learn_nodes = response.xpath('//div[@class="item"]')
        for learn_node in learn_nodes:
            yield{
                'content：' : "".join(str(learn_node.css('h5 > a::text').extract_first()).split()) ,
                'source:' : learn_node.css('p.source-book>span.link>a::text').extract_first(),
                'from :' : str(learn_node.css('p.source-book>span.link:nth-child(2) >a::text').extract_first())
                # '來源：' : learn_node.css('p.source-book>span.link>a::text').extract_first(),
                # '作者：' : learn_node.css('p.source-book>span.link:nth-child(2) >a::text').extract_first()
            }


# class booksSpider(scrapy.Spider):
#     name = "quotes"
#     allowed_domains = ["quotes.toscrape.com"]
#     start_urls = [
#         "http://quotes.toscrape.com/"
#     ]
#
#     # def parse(self, response):
#     #     filename = response.url.split("/")[-2]
#     #     with open(filename, 'wb') as f:
#     #         f.write(response.body)
#
#     # def parse(self, response):
#     #     # learn_nodes = response.css('div.item')
#     #     learn_nodes = response.xpath('//div[@class="quote"]')
#     #     for learn_node in learn_nodes:
#     #         yield{
#     #             '英文名言' : learn_node.css('span.text::text').extract_first()
#     #         }
#     def parse(self, response):
#     #使用 css 選擇要素進行抓取，如果喜歡用BeautifulSoup之類的也可以
#     #先定位一整塊的quote，在這個網頁塊下進行作者、名言,標籤的抓取
#         for quote in response.css('.quote'):
#             yield {
#                 '作者' : quote.css('small.author::text').extract_first(),
#                 'tags' : quote.css('div.tags a.tag::text').extract(),
#                 '英文名言' : quote.css('span.text::text').extract_first()
#             }
