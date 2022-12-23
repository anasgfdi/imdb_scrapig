import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapingImdbItem


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['www.imdb.com']
    custom_settings = {  "ITEM_PIPELINES": {'scraping_imdb.pipelines.MoviesPipeline': 300}
                        }   
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'


    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })


    # le_movie_detail=LinkExtractor(restrict_xpaths="//td[@class='titleColumn']")
    rule_movie_detail=Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"),
                        callback='parse_item',
                        follow=False)


    rules = (
        rule_movie_detail,
    )

    def parse_item(self, response):

        items= ScrapingImdbItem()

        items['title']= response.xpath('//h1/text()').get()
        items['original_title']= response.xpath('//div[@class="sc-dae4a1bc-0 gwBsXc"]/text()').get()
        items['score']= response.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()').get()
        items['genre']= response.xpath('//span[@class="ipc-chip__text"]/text()').getall()
        items['date']= response.xpath('//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"]/text()').get()
        items['synopsis']=response.xpath('//span[@class="sc-16ede01-1 kgphFu"]/text()').get()

        duree_list = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()').extract()

        if len(duree_list)>2:
            items['duree']= int(duree_list[0])*60 + int(duree_list[3])
        else:
            items['duree']= int(duree_list[0]) 


        items['casting']=response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()').getall()

        items['pays']=response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section/div[2]/ul/li[2]/div/ul/li/a/text()').extract()[:-1]

        yield items