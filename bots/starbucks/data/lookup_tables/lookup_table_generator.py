"""Generate lookup tables for item names and option names based on menu."""
import json

with open("../menus/starbucks.json") as f:
    # get item names
    menu = json.load(f)
    keys = menu.keys()
    with open("./starbucks_items.txt", 'w') as fout:
        fout.write("\n".join(menu))

    # get options
    options = set()
    for v in menu.values():
        options.update(v['options'].keys())
    unique_options = options - {'Short', 'Tall', 'Grande', 'Venti', 'Trenta'}
    with open("./starbucks_options.txt", 'w') as fout:
        for o in unique_options:
            fout.write(o + '\n')
