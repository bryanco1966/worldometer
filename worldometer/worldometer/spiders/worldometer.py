# -*- coding: utf-8 -*-
import scrapy


class WorldometerSpider(scrapy.Spider):
    name = 'worldometer'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #this creates a response object that contains both the text and
        # a href
        countries = response.xpath('//td/a')
        for country in countries:
            #must use dot preceding slashes when not using the response
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            #link is a relative url can either create a full url  with following
            # or use response follow
            #absolute_url = f"https://www.worldometers.info{link}"
            #absolute_url = response.urljoin(link)
            #yield scrapy.Request(url = absolute_url)
            yield  response.follow( url = link, callback=self.parse_country, meta={"country_name" : name})

    def parse_country(self, response):
        #go through the years of the populations  first need to isolate table
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        name = response.request.meta['country_name']
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
            'name' : name,
            'year': year,
            'population': population
            }
