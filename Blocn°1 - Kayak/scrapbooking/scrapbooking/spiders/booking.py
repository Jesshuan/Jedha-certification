import scrapy
import re
import numpy as np


# - IMPORTATION DE LA LISTE DES VILLES - 
list_city=['Marseille','Paris']

# - SPIDER -
class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/index.fr.html/']

    
    def parse(self, response):
        # fonction parse d'entrée sur le site - on remplit la première destination de la liste
        # (pour nous, dans ce cas, il s'agit d'une fonction d'initialisation !)
        iter=0
        return scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_city[0]}, # - on utilise le champs 'ss' pour remplir le champs
                callback=self.change_url_hostels, # - fonction appelée 'change_url_hostels', une fois que l'on sera dans la page de la première destination de la liste
                meta={'iter':iter} # - on définit une variable itérative à 0, cette variable 'iter' sera notre intérateur sur les destinations de la liste
            )
    

    def change_url_hostels(self, response):
        # cette fonction s'emploi dès qu'on atterit dans une nouvelle page de destination, pour changer l'url
        # à partir de l'url en place, afin de ne visualiser que les hôtels sur les 25 lieux de réservations affichés 

        iter=response.request.meta['iter'] # on récupère notre itérable, pour le réattribuer non modifié dans le yield suivant

        url_dest=response.url # on récupère l'url en place
        yield response.follow(url_dest + '&nflt=ht_id%3D204', # on ajoute à l'url en place la variable de tri d'hotels
                                callback=self.parse_my_dest, # on appelle la fonction de parse spéciale pour les pages de listes de lieux pour une destination
                                meta={'iter':iter})

    
    def parse_my_dest(self, response):
        # fonction appelée quand nous sommes, à chaque fois, sur une page de city avec la liste (exclusivement) des hôtels

        iter=response.request.meta['iter'] # on récupère notre itérable dans le champs méta

        city_and_nb_hostels = response.xpath('//div[@class=\'d8f77e681c\']/text()').get().split(' ')
        city = re.sub("\s+|\'|\?|\:","",str(city_and_nb_hostels[0])).lower()
        #nb_hostels = int(city_and_nb_hostels[1])

        # Petite précaution pour s'assurer, pendant les tests, que le nom de ville est indentique au nom de ville dans notre liste initiale
        if city!=list_city[iter].lower():
            print("WARNING ! Perhaps {} is not the same city than {}...".format(city,list_city[iter]))

        path_base='//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[*]'
        list_hostels=response.xpath(path_base + '/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()').getall()
        list_hostels_urls=response.xpath(path_base + '/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/@href').getall()
        list_hostels_img=response.xpath(path_base + '/div/div/div/a/img/@src').getall()
        list_hostel_alt_img=response.xpath(path_base + '/div/div/div/a/img/@alt').getall()
        #list_hostel_text=response.xpath(path_base + '/div/div[2]/div/div/div/div/div[4]/text()').getall()
        list_hostel_review=response.xpath(path_base + '/div/div[2]/div/div/div[2]/div/a/span/div/div/text()').getall()
        
        for i, link in enumerate(list_hostels_urls):

            try:
                yield response.follow(link,
                                    callback=self.in_hostel_page,
                                    meta={'city':list_city[iter],
                                        'hostel_name':list_hostels[i],
                                        'hostel_img':list_hostels_img[i],
                                        'hostel_alt_img':list_hostel_alt_img[i],
                                        #'hostel_text':list_hostel_text[i],
                                        'hostel_review':list_hostel_review[i],
                                        'hostel_url':link})

            except:
                yield {
                'city':list_city[iter],
                'hostel_name':list_hostels[i],
                'hostel_url':link,
                'hostel_img':list_hostels_img[i],
                'hostel_alt_img':list_hostel_alt_img[i],
                #'hostel_text':list_hostel_text[i],
                'hostel_review':list_hostel_review[i],
                'nb_squares':np.nan,
                'nb_stars':np.nan,
                'hostel_url':link,
                'hostel_type':np.nan,
                'lat_long':np.nan,
                'description':np.nan}

        iter+=1
        if iter<=len(list_city)-1:

            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': list_city[iter]},
                callback=self.change_url_hostels,
                meta={'iter':iter}
            )

    def in_hostel_page(self,response):

        city=response.request.meta['city']
        hostel_name=response.request.meta['hostel_name']
        hostel_url=response.request.meta['hostel_url']
        hostel_img=response.request.meta['hostel_img']
        hostel_alt_img=response.request.meta['hostel_alt_img']
        #hostel_text=response.request.meta['hostel_text']
        hostel_review=response.request.meta['hostel_review']

        type=response.xpath('//span[@class=\'e2f34d59b1\']/text()').get()
        lat_long=response.xpath('//a[@id=\'hotel_surroundings\']/@data-atlas-latlng').get()
        description=response.xpath('//*[@id=\'property_description_content\']/p[2]/text()').get()

        nb_squares=len(response.xpath('//*[@data-testid=\'rating-squares\']/span[*]').getall())
        nb_stars=len(response.xpath('//*[@data-testid=\'rating-stars\']/span[*]').getall())
        
        yield {
                'city':city,
                'hostel_name':hostel_name,
                'hostel_url':hostel_url,
                'hostel_img':hostel_img,
                'hostel_alt_img':hostel_alt_img,
                #'hostel_text':hostel_text,
                'hostel_review':hostel_review,
                'nb_squares':nb_squares,
                'nb_stars':nb_stars,
                'hostel_type':type,
                'lat_long':lat_long,
                'description':description
            }
