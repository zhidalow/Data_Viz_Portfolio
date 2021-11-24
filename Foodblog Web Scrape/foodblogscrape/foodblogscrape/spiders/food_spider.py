import scrapy


class FoodSpider(scrapy.Spider):
    #spider name; must be unique. Used to call from cmd line later
    name = 'foodinfo'

    #start url pg to scrape from
    start_urls = ['https://www.misstamchiak.com/eat/']

    #init iterator variables to stop spider after scraping ALL links in COUNT_MAX pages
    count=0
    COUNT_MAX=2

    def parse(self, response):

            #get href links to desired posts, then parse responses from each link and store in json obj during callback
            food_page_links = response.css('.masonry-item').xpath('.//div[@class="read-more-link"]/a/@href').getall() 
            yield from response.follow_all(food_page_links, callback=self.parse_food_page_links)
            self.count += 1

            #only move on to next pg to scrape if pg cnt limit has not been reached
            if (self.count < self.COUNT_MAX):
                pagination_links = response.css('a.nextpostslink::attr(href)').getall()
                yield from response.follow_all(pagination_links, callback=self.parse)

    #parse css objects to retireve desired data from webpage
    def parse_food_page_links(self, response):
        
        #helper function extract_with_css to return empty obj if no element found in pg
        def extract_with_css(query):
            return response.css(query).get(default='')

        yield {
            'title': extract_with_css('title::text'),
            'site_url': extract_with_css('meta[property*="og:url"]::attr(content)'),
            'storename': extract_with_css('h3.company-name__label span::text'),
            'address': extract_with_css('.company-address::text'),
            'area': extract_with_css('.company-area::text'),
            'opening_hours': extract_with_css('.company-opening_hours::text'),
            'cuisine': extract_with_css('.company-cuisine::text'),
        }
        