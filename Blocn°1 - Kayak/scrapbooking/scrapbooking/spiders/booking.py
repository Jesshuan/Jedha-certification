import scrapy
import re
import numpy as np

list_city=['Marseille','Aix-en-Provence','Paris','Toulouse','Dijon']

class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/index.fr.html']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_city[0]},
                callback=self.after_search,
                meta={'iter':0}
            )
    
    def after_search(self, response):

        iter=response.request.meta['iter']

        city_and_nb_hostels = response.xpath('//div[@class=\'d8f77e681c\']/text()').get().split(' ')
        city = re.sub("\s+|\'|\?|\:","",str(city_and_nb_hostels[0])).lower()
        nb_hostels = int(city_and_nb_hostels[1])

        if city!=list_city[iter].lower():
            print("WARNING ! Perhaps {} is not the same city than {}...".format(city,list_city[iter]))
        
        for h in range (20):
            good_div = '//div[@class="d4924c9e74"]/div[{}]'.format(2*h+3)
            hostel_name = response.xpath(good_div + '/div/div[2]/div/div/div/div/div/div/h3/a/div/text()').get()
            
            try:
                hostel_url = response.xpath(good_div + '/div/div[2]/div/div/div/div/div/div/h3/a').attrib["href"]
                yield response.follow(hostel_url,
                                    callback=self.in_hostel_page,
                                    meta={'city':city,
                                        'hostel_name':hostel_name})
            except:
                yield {
                'city':city,
                'hostel_name':hostel_name,
                'hostel_type':np.nan
            }

        iter+=1
        if iter<=len(list_city)-1:

            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_city[iter]},
                callback=self.after_search,
                meta={'iter':iter}
            )

    def in_hostel_page(self,response):
        type=response.xpath('//span[@class=\'e2f34d59b1\']/text()').get()

        city=response.request.meta['city']
        hostel_name=response.request.meta['hostel_name']

        yield {
                'city':city,
                'hostel_name':hostel_name,
                'hostel_type':type
            }