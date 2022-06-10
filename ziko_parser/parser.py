import re
from base_parser import BaseParser


class ZikoParser(BaseParser):

    def __init__(self, extra_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_url = extra_url
        self.response_url = self.get_response(self.url)
        self.response_extra_url = self.get_response(self.extra_url)

    @staticmethod
    def prepare_work_hours(template, saturday='nie'):
        prepared_template = template.strip('<br>').split('<br>')
        result = []
        for item in prepared_template:
            if saturday in item:
                nie_hour = prepared_template.pop().strip()
                result.append(f'{saturday} {nie_hour}')
                break
            else:
                result.append(item)
        return result

    def get_data(self):
        result = []
        phones = re.findall(r'tel\.\s+(.{12})', self.response_extra_url.text)
        for pharmacy, phone in zip(self.response_url.json().values(), phones):
            street = pharmacy.get('address')
            city = pharmacy.get('city_name')
            address = f'{street}, {city.pop()}'
            lat = pharmacy.get('lat')
            lng = pharmacy.get('lng')
            name = pharmacy.get('title')

            raw_working_hours = pharmacy.get('mp_pharmacy_hours')
            prepared_working_hours = self.prepare_work_hours(raw_working_hours)

            result.append(
                (address, [lat, lng], name, [phone], prepared_working_hours)
            )
        return result
