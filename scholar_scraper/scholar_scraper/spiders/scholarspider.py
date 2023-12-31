import scrapy
from scholar_scraper.items import ScholarScraperItem
import w3lib.html


class ScholarspiderSpider(scrapy.Spider):
    name = "scholarspider"
    allowed_domains = ["scholar.google.com"]
    start_urls = ["https://scholar.google.com/"]
    result_index = 0


    def parse(self, response, result_index=0):

        query = input('Search keyword: ').replace(' ', '+')
        result_limit = int(input('Maximum number of results: '))

        for count, value in enumerate(range(result_limit)):

            if  < result_limit:
                next_page_url = 'https://scholar.google.com/scholar?start='+str(count*20)+'&q='+query+'+&hl=en&as_sdt=0,5'
                yield scrapy.Request(next_page_url, callback=self.parse_page)
            else:
                yield





    def parse_page(self, response):
        results = response.css('div.gs_ri')

        for result in results:
            result_item = ScholarScraperItem()

            result_item['title'] = w3lib.html.remove_tags(result.css('h3 a').get())
            result_item['url'] = result.css('h3 a ::attr(href)').get()
            result_item['description'] = w3lib.html.remove_tags(result.css('div.gs_rs').get())
            result_item['author'] = result.css('div.gs_a a::text').get()

            # THIS NEEDS TO BE WORKED ON; IT ADDS MULTIPLE AUTHOR ITEM FIELDS BASED ON NUMBER OF AUTHORS
            # a_list = result.css('div.gs_a a')
            # authors = ''
            # for index, author in enumerate(a_list):
            #     result_item['author'] = result.css('div.gs_a a::text').get()

            ##Checking for empty items and using alternative methods for retrieving them:
            if result_item['author'] is None:
                # this line gets the raw text of the subheading data then splits it
                # based off the delimiter '\xa0-' and takes the first item of the resulting string list
                result_item['author'] = result.css('div.gs_a::text').get().split('\xa0-', 1)[0]

            count += 1
            yield result_item