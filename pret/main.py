__author__ = 'Rachid Belaid'

import urllib2
from BeautifulSoup import BeautifulSoup
from termcolor import colored


def display_menu(kcal):
    page = urllib2.urlopen("http://pret.com/menu/")
    soup = BeautifulSoup(page)
    product_categories= soup.findAll('div', { "class" : "product_category" })
    menu= {}
    for product_category in product_categories :
        category=product_category.img['alt']
        menu[category] = []
        foods = product_category.findAll('a')
        for food in foods :
            if kcal :
                page = urllib2.urlopen('http://pret.com/%s'%food['href'])
                food_page = BeautifulSoup(page)
                food_kcal=food_page.findAll('td',{"class": "nutr_value"})[0].text
                food_tuple=(food.text,food_kcal)
            else :
                food_tuple=(food.text,)
            menu[category].append(food_tuple)
            print "%s %s %s" % (colored("[%s]"%category.upper(),'yellow'),food_tuple[0],'') + colored("(%s kcal)"%food_tuple[1],'red') if kcal else ''





if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-k", "--kcal",
                      action="store_true", dest="kcal", default=False,
                      help="print the kcal associate in the menu")
    parser.add_option("-m", "--menu",action="store_true",dest="menu", default=False,
                      help="display list of pret.com menu")


    (options, args) = parser.parse_args()
    if options.menu:
        display_menu(options.kcal )
        