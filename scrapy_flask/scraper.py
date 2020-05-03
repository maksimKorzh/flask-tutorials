#
# Alexander's spider code with CMK additions
# CMK's code is commented
#

#
# The request was to pass arguments "acupuncturist" & "counselor" to spider
#


import scrapy

# use crrawler process to run spider from within a python script
from scrapy.crawler import CrawlerProcess

# needed to parse settings
import json

class Wellness(scrapy.Spider):
    name = "wellness"
    allowed_domains = ["wellness.com"]  

    def start_requests(self):
        # reset output file
        with open('wellness.jsonl', 'w') as f:
            f.write(' ')
    
        # settings content
        settings = ''
        
        # load settings from local file
        with open('settings.json', 'r') as f:
            for line in f.read():
                settings += line
        
        # parse settings
        settings = json.loads(settings)
        yield scrapy.Request('https://www.wellness.com/find/%s' % settings['category'], callback=self.state)
            
    def state(self, response):
        for a in response.css("div.find-item-container a")[0:15]:
            yield response.follow(a, callback=self.city)
            
    def city(self, response):
        for a in response.css("li.categories-li a"):
            yield response.follow(a, callback=self.profile_link)
            
    def profile_link(self, response):
        for a in response.css("h2 a"):
            yield response.follow(a, callback=self.profile)
            
        next_page = response.css("li.pagination-next a")
        if next_page is not None:
            yield response.follow(next_page, self.profile_url)

    def profile(self, response):
        services = response.xpath('.//span[contains(text(),"Services")]')
        education = response.xpath('.//span[contains(text(),"Education")]')
        training = response.xpath('.//span[contains(text(),"Training")]')

        # init item
        item = {}
        
        item['First_and_Last_Name'] = response.css('h1::text').get()
        item['About'] = response.css('.listing-about::text').get()
        item['Services'] = services.xpath('following-sibling::span[1]/text()').extract()
        item['Primary_Specialty'] = response.css('.normal::text').get()
        item['Practice'] = response.css('.years-in-service::text').get()
        item['Education'] = education.xpath('following-sibling::span[1]/text()').extract()
        item['Training'] = training.xpath('following-sibling::span[1]/text()').extract()

        review_link = response.css('#reviews_tab a::attr(href)').get()
        if review_link is not None:
            yield scrapy.Request(response.urljoin(review_link), callback=self.parse_reviews, meta={'item': item})
        else:
            directions_link = response.css('#directions_tab a::attr(href)').get()
            yield scrapy.Request(response.urljoin(directions_link), callback=self.parse_directions, meta={'item': item})

    def parse_reviews(self, response):
        item = response.meta['item']
        item['Consumer_Feedback'] = response.css('.item-rating-container a::text').get() 

        directions_link = response.css('#directions_tab a::attr(href)').get()
        yield scrapy.Request(response.urljoin(directions_link), callback=self.parse_directions, meta={'item': item})

    def parse_directions(self, response):
        item = response.meta['item']
        item['Phone'] = response.css('.tel::text').get()
        item['Address'] = response.css('.item-separator+ span::text').get()
        
        # write output file
        with open('wellness.jsonl', 'a') as f:
            f.write(json.dumps(item, indent=2) + '\n')
        
        
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Wellness)
    process.start()       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
