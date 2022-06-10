from pathlib import Path
from kfc_parser.parser import KFCParser
from monomax_parser.parser import MonomaxParser
from ziko_parser.parser import ZikoParser


def get_save_dir(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    return dir_path


if __name__ == "__main__":
    keys = ('address', 'latlon', 'name', 'phones', 'working_hours')
    dir_names = ('kfc_parser', 'ziko_parser', 'monomax_parser')
    kfc_url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
    monomax_url = 'https://monomax.by/map'
    ziko_url = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'
    ziko_extra_url = 'https://www.ziko.pl/lokalizator/'
    save_path_kfc, save_path_ziko, save_path_monomax = map(get_save_dir, dir_names)

    monomax = MonomaxParser(monomax_url, save_path_monomax, keys)
    kfc = KFCParser(kfc_url, save_path_kfc, keys)
    ziko = ZikoParser(ziko_extra_url, ziko_url, save_path_ziko, keys)

    monomax_data = monomax.prepare_to_json(monomax.get_data())
    monomax.update_json(monomax_data)

    kfc_data = kfc.prepare_to_json(kfc.get_data())
    kfc.update_json(kfc_data)

    ziko_data = ziko.prepare_to_json(ziko.get_data())
    ziko.update_json(ziko_data)







