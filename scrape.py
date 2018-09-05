import string
import requests
from bs4 import BeautifulSoup


class InvestopediaScrape:
    def __init__(self):
        print("Starting...", flush=True)
        self.fh = open('output.txt', 'w', encoding="utf-8")

    def scrape(self, alphabet):
        r = requests.get('https://www.investopedia.com/terms/{}/'.format(alphabet))
        soup = BeautifulSoup(r.text, "html5lib")
        try:
            page = soup.find('li', {'class': 'pager-last last'}).find('a')['href'].split('=')[1]
        except:
            page = 1
            pass
        for page_number in range(0, int(page)):
            r = requests.get('https://www.investopedia.com/terms/{}/?page={}'.format(alphabet, page_number))
            encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
            soup = BeautifulSoup(r.content, "html5lib", from_encoding=encoding)
            text = [term.text.strip() for term in soup.findAll('h3', {'class': 'item-title'})]
            self.fh.write(','.join(text))
            self.fh.write('\n')

    def close(self):
        self.fh.close()

if __name__ == '__main__':
    crawler = InvestopediaScrape()
    for alphabet in list(string.ascii_lowercase):
        print("Fetching words starting with: {}".format(alphabet), flush=True)
        crawler.scrape(alphabet)
    crawler.close()
    print('Done!')
