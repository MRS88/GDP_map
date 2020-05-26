''' Вывод интерактивной карты мира с ВВП стран'''
import json
import pygal

from pygal.style import RotateStyle as RS
from pygal.style import LightColorizedStyle as LCS
from country_codes import get_country_code


filename = 'gdp_json.json'
with open(filename) as f:
    gdp_data = json.load(f)

# Построение словаря с данными ВВП
cc_gdp_value = {}
for gdp_dict in gdp_data:
    if gdp_dict['Year'] == 2014:
        country_name = gdp_dict['Country Name']
        gdp_value = round(gdp_dict['Value'] / 1000000000, 2)
        code = get_country_code(country_name)
        if code:
            cc_gdp_value[code] = gdp_value

# Группировка стран по уровню ВВП
cc_gdp_1, cc_gdp_2, cc_gdp_3, cc_gdp_4, cc_gdp_5 = {}, {}, {}, {}, {}
for cc, gdp in cc_gdp_value.items():
    if gdp < 100:
        cc_gdp_1[cc] = gdp
    if gdp < 500:
        cc_gdp_2[cc] = gdp
    if gdp < 1000:
        cc_gdp_3[cc] = gdp
    if gdp < 3000:
        cc_gdp_4[cc] = gdp
    else:
        cc_gdp_5[cc] = gdp

# Проверка количества стран на каждом уровне
print(len(cc_gdp_1), len(cc_gdp_2), len(cc_gdp_3),len(cc_gdp_4),        len(cc_gdp_5))

wm_style = RS('#339966', base_style=LCS)
wm = pygal.maps.world.World(style=wm_style)
wm.title = 'ВВП стран на 2014 год, млрд.долл'
wm.add('< 100 млрд.долл', cc_gdp_1)
wm.add('100-500 млрд.долл', cc_gdp_2)
wm.add('500-1000 млрд.долл', cc_gdp_3)
wm.add('1-3 трлн.долл', cc_gdp_4)
wm.add('3< трлн.долл', cc_gdp_5)
wm.add('Нет данных', ['gf', 'ly', 'sy', 'er', 'kp', 'tw', 'gf', 'eh', 'aq'])
wm.render_to_file('world_gdp.svg')
