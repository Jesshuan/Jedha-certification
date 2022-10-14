import scrapy
import pandas as pd


# - IMPORTATION DE LA LISTE DES VILLES -
list_src = pd.read_csv('./../../../src/top35_list_cities.txt').reset_index()

list_cities = list_src['Cities'].to_list()


# - SPIDER -
class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/index.fr.html/']

    
    def parse(self, response):
        # fonction parse d'entrée sur le site - on remplit la première destination de la liste
        # (pour nous, dans ce cas, il s'agit d'une fonction qui ne sera utilisée qu'une fois)
        iter=0
        return scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_cities[0]}, # - on utilise le champs 'ss' pour remplir le champs avec la première destination
                callback=self.change_url_hostels, 
                meta={'iter':iter} # - on définit une un itérable à 0, itérateur sur les destinations de la liste
            )
    

    def change_url_hostels(self, response):
        # fonction appelée dès qu'on atterit dans une nouvelle page de destination
        # objectif : changer l'url pour ne visualiser que des hôtels

        iter=response.request.meta['iter'] # on récupère notre variable méta : l'itérable

        url_dest=response.url # on récupère l'url en place
        yield response.follow(url_dest + '&nflt=ht_id%3D204', # on ajoute à l'url en place la variable qui filtre les hotels
                                callback=self.parse_my_dest, 
                                meta={'iter':iter})

    
    def parse_my_dest(self, response):
        # fonction appelée sur une page de city avec la liste (exclusivement) des hôtels

        iter=response.request.meta['iter'] # on récupère notre itérable dans le champs méta

        list_hostels_urls=response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[*]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/@href').getall()
        #on scrap la liste des 25 urls d'hotels de la page en une seule fois, grâce à l' * et à getall()

        for i, link in enumerate(list_hostels_urls):
            # pour chaque lien/hotel de la page, on appelle une fonction de scraop dans la page de l'hotel
            yield response.follow(link,
                                callback=self.in_hostel_page,
                                meta={'city':list_cities[iter],'hostel_url':link}) # transport avec meta du nom de la ville et du lien de l'hotel

        iter+=1
        if iter<=len(list_cities)-1:
        # quand les 25 links/hotels sont scrappés, on itère notre variable en vue de la prochaine destination
        # la prochaine destination est rempli dans le Form de la page en cours
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_cities[iter]},
                callback=self.change_url_hostels,
                meta={'iter':iter} # transport avec méta de l'itérable
            )

    def in_hostel_page(self,response):
    # fonction appelée quand on atterit sur une page propre à l'hotel

        # redéploiement des variables méta - qui feront parties du yield final
        city=response.request.meta['city']
        hostel_url=response.request.meta['hostel_url']

        # scrapping de toutes les infos recherchées
        hostel_name=response.xpath('//div[@id="hp_hotel_name"]/div/div/h2/text()').get()
        hostel_img=response.xpath('//div[@id="hotel_main_content"]/div/div/div[3]/a/img/@src').get()
        hostel_alt_img=response.xpath('//div[@id="hotel_main_content"]/div/div/div[3]/a/img/@alt').get()
        hostel_review=response.xpath('//div[@data-testid="review-score-right-component"]/div/text()').get()
        type=response.xpath('//span[@class=\'e2f34d59b1\']/text()').get()
        lat_long=response.xpath('//a[@id=\'hotel_surroundings\']/@data-atlas-latlng').get()
        description=response.xpath('//*[@id=\'property_description_content\']/p[2]/text()').get()
        # ici on compte le nombre d'étoiles ou de carrés de l'hôtel, pour un éventuel classement
        nb_squares=len(response.xpath('//*[@data-testid=\'rating-squares\']/span[*]').getall())
        nb_stars=len(response.xpath('//*[@data-testid=\'rating-stars\']/span[*]').getall())
        
        # yield final
        yield {
                'city':city,
                'hostel_name':hostel_name,
                'hostel_url':hostel_url,
                'hostel_img':hostel_img,
                'hostel_alt_img':hostel_alt_img,
                'hostel_review':hostel_review,
                'nb_squares':nb_squares,
                'nb_stars':nb_stars,
                'hostel_type':type,
                'lat_long':lat_long,
                'description':description
            }
