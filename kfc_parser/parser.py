from base_parser import BaseParser
from .templates import workday_template, holiday_template


class KFCParser(BaseParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = self.get_response(self.url)

    @staticmethod
    def prepare_work_hours(templates, regular):
        result = []
        for temp in templates:
            result.append(temp.format(*map('{:.5}'.format, regular)))
        return result

    def get_data(self):
        result = []
        restaurants = [rest.get('storePublic') for rest in self.response.json().get('searchResults')]
        for rest in restaurants:
            name = rest.get('title').get('ru')
            contacts = rest.get('contacts')
            open_hours = rest.get('openingHours')
            is_closed = rest.get('status')

            address = contacts.get('streetAddress').get('ru')
            latlon = contacts.get('coordinates').get('geometry').get('coordinates')

            # phones = contacts.get('phoneNumber')
            try:
                phone = contacts.get('phone').get('number').split()
                extra_phones = contacts.get('phone').get('extensions')
                phone.extend(extra_phones)
            except AttributeError:
                phone = []

            regular = open_hours.get('regular').values()
            templates = workday_template, holiday_template
            working_hours = self.prepare_work_hours(templates, regular) if all(regular) else is_closed.lower()

            result.append(
                (address, latlon, name, phone, working_hours)
            )
        return result
