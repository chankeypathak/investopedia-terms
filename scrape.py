import string
import requests
from bs4 import BeautifulSoup


class InvestopediaScrape:
    def __init__(self):
        print("Starting...")

    def scrape(self, alphabet):
        r = requests.get('https://www.investopedia.com/terms/{}/'.format(alphabet))
        soup = BeautifulSoup(r.text, "html5lib")
        page = soup.find('li', {'class': 'pager-last last'}).find('a')['href'].split('=')[1]
        for page_number in range(0, int(page)):
            r = requests.get('https://www.investopedia.com/terms/{}/?page={}'.format(alphabet, page_number))
            soup = BeautifulSoup(r.text, "html5lib")
            text = [term.text.strip() for term in soup.findAll('h3', {'class': 'item-title'})]
            return ','.join(text)


if __name__ == '__main__':
    crawler = InvestopediaScrape()
    for alphabet in list(string.ascii_lowercase):
        with open('output.csv', 'w') as fh:
            fh.write(crawler.scrape(alphabet))
    print('Done!')