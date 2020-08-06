"""Generate a Chatette template from the scraped JSON Taco Bell menu."""

import sys
import json

from collections import defaultdict

menu_path = sys.argv[1]
out_path = sys.argv[2]

with open(menu_path) as f:
    menu_data = json.load(f)

option_map = defaultdict(set)
option_names = defaultdict(set)
option_names['size'] = set(['Small', 'Medium', 'Large'])

for product_name, value in menu_data.items():
    if value.get('addons') and value.get('sauces'):
        option_map['with_sauces_and_addons'].add(product_name)
    if value.get('addons'):
        option_map['with_addons'].add(product_name)
        option_names['addon'].update([addon['name']
                                      for addon in value['addons']])
    if value.get('sauces'):
        option_map['with_sauces'].add(product_name)
        option_names['sauce'].update([sauce['name']
                                      for sauce in value['sauces']])
    if value.get('sizes'):
        option_map['with_sizes'].add(product_name)

lines = []
for k, v in option_map.items():
    lines.append('@[product#{}]'.format(k))
    for name in v:
        lines.append('    {}'.format(name))
for k, v in option_names.items():
    lines.append('@[{}]'.format(k))
    for name in v:
        lines.append('    {}'.format(name))
lines.append('@[menu_category]')
for category_name in menu_data['menu_categories']:
    lines.append('    {}'.format(category_name))

with open(out_path, 'w') as f:
    f.write('\n'.join(lines))
