import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapingImdbItem


class TvShowsSpider(CrawlSpider):
    name = 'tv_shows'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/', headers={
            'User-Agent': self.user_agent
        })


    # le_movie_detail=LinkExtractor(restrict_xpaths="//td[@class='titleColumn']")
    rule_tvshows_detail=Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"),
                        callback='parse_item',
                        follow=False)


    rules = (
        rule_tvshows_detail,
    )

    def parse_item(self, response):

        items= ScrapingImdbItem()

        items['title']= response.xpath('//h1/text()').get()
        items['original_title']= response.xpath('//div[@class="sc-dae4a1bc-0 gwBsXc"]/text()').get()
        items['score']= response.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()').get()
        items['genre']= response.xpath('//span[@class="ipc-chip__text"]/text()').getall()
        items['date']= response.xpath('//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"]/text()').get()
        items['synopsis']=response.xpath('//span[@class="sc-16ede01-1 kgphFu"]/text()').get()

             
        duree_list = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()").extract()
        if len(duree_list)==5:
            items['duree']= int(duree_list[0])*60 + int(duree_list[3])
        else:
            items['duree']= int(duree_list[0]) 



        if items['genre'] == 'Documentary' or 'Game-show':
            items['casting']=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li/div/ul/li/a/text()').getall()
        else:
            items['casting']=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[2]/div/ul/li/a/text()').getall()

        items['pays']=response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section/div[2]/ul/li[2]/div/ul/li/a/text()').extract()[:-1]




        yield items
