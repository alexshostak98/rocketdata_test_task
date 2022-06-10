from base_parser import BaseParser
import re
import bs4


class MonomaxParser(BaseParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = self.get_response(self.url)

    def get_soup(self):
        return bs4.BeautifulSoup(self.response.text, 'lxml')

    def get_data(self):
        name = 'Мономах'
        result = []
        soup = self.get_soup()
        shops_soup = soup.find_all('div', attrs={'class': 'shop'})
        latlons = re.findall(r'\n\s*(\[.*\])', self.response.text)
        for shop, latlon in zip(shops_soup, latlons):
            address, phone = shop.text.strip().split('\n')
            latlon = [float(item) for item in latlon.strip('[]').split(',')]

            result.append(
                (address, latlon, name, [phone])
            )
        return result
