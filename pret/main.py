import socket
import thread
import time

__author__ = 'Rachid Belaid'

import urllib2
from BeautifulSoup import BeautifulSoup
from termcolor import colored


def display_menu(kcal):
    page = urllib2.urlopen("http://pret.com/menu/")
    soup = BeautifulSoup(page)
    product_categories = soup.findAll('div', {"class": "product_category"})
    menu = []
    for product_category in product_categories:
        category = product_category.img['alt']
        foods = product_category.findAll('a')
        for food in foods:
            if kcal:
                page = urllib2.urlopen('http://pret.com/%s' % food['href'])
                food_page = BeautifulSoup(page)
                food_kcal = food_page.findAll('td', {"class": "nutr_value"})[0].text
                food_tuple = (food.text, food_kcal)
            else:
                food_tuple = (food.text,)
            menu.append(food_tuple)
            display = ("%s %s %s") % (colored("[%s]" % category.upper(), 'yellow'),
                                      food_tuple[0],
                                      (colored("(%s kcal)" % food_tuple[1], 'red') if kcal else ''),
                )
            print "%s %s" % (display.ljust(90, '.'), (colored("[%s]" % len(menu), 'green')))
    return menu


def wait_to_order():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_socket.bind(('', 8881))

    print 'Waiting for somebody to collect order ...'
    order_server = None
    while not order_server:
        message, address = my_socket.recvfrom(8881)
        order_server = str(address[0])
    return order_server


def broadcast():
    while True:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        my_socket.sendto('I m hungry', ('<broadcast>', 8881))
        time.sleep(1)


def start_server():
    from SimpleXMLRPCServer import SimpleXMLRPCServer

    name = raw_input('What is your name --> ')

    def order(name, baskets):
        for item in baskets:
            print ("%s %s") % (colored('[%s]' % name, 'green'), colored('%s' % item, 'yellow'))
        return True

    def who():
        return name

    server = SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()), 8000), logRequests=False)
    print "Listening order ..... "
    server.register_function(who, "who")
    server.register_function(order, "order")
    server.serve_forever()


def main():
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-k", "--kcal",
                      action="store_true", dest="kcal", default=False,
                      help="print the kcal associate in the menu")
    parser.add_option("-m", "--menu", action="store_true", dest="menu", default=False,
                      help="listen the menu only")
    parser.add_option("-l", "--listen", action="store_true", dest="listen", default=False,
                      help="listen order of pret.com menu")

    (options, args) = parser.parse_args()

    if options.listen:
        thread.start_new_thread(broadcast, ())
        start_server()
    else:
        menu = display_menu(options.kcal)
        if not options.menu:
            order_server = wait_to_order()
            import xmlrpclib

            proxy = xmlrpclib.ServerProxy("http://%s:8000/" % order_server)
            listener = proxy.who()
            name = raw_input('What is your name --> ')
            checkout = False
            baskets = []
            while not checkout:
                order = raw_input('What do you want to order --> ')
                if not order.isdigit():
                    continue
                order = int(order)
                conf = ''
                while not str(conf).upper() in ['Y', 'N']:
                    conf = raw_input('Do you confirm the "%s"  ? (Y/N) --> ' % menu[int(order) - 1][0])
                if  str(conf).upper() == 'Y':
                    baskets.append(menu[order - 1])
                checkout = True if str(
                    raw_input('Do you want to order something else ? (Y/N)--> ')).upper() == 'N' else False

            print "ORDER RESUME".center(60, "=")
            for item in baskets:
                print item[0]
            send = raw_input('Do you want to send this order ? (Y/N)--> ')
            if send:
                if proxy.order(name, baskets):
                    print "ORDER RECEIVED BY %s" % listener

if __name__ == '__main__':
    main()