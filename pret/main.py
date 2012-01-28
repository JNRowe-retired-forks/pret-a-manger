__author__ = 'Rachid Belaid'




import urllib2
from BeautifulSoup import BeautifulSoup


def main():
    page = urllib2.urlopen("http://pret.com/menu/new_food_at_pret/chicken_pesto_bloomer_PUK4451.shtm")
    soup = BeautifulSoup(page)
    table= soup.find('table', id="nutritional_table")
    rows = table.findAll('tr')
    list = []
    for tr in rows:
      cols = tr.findAll('td')
      t = []
      for td in cols:
          text = ''.join(td.find(text=True))
          t.append(text)
      list.append(tuple(t))
    print list


if __name__ == '__main__':
    main()