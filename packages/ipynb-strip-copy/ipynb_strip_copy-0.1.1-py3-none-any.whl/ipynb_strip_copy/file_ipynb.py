import json
import pathlib
from copy import deepcopy

from ipynb_strip_copy.search_apply import search_apply_command, ORIG_CMD_STRIP


def search_apply_json(json_dict):
    source_list = [''.join(d['source']) for d in json_dict['cells']]

    suffix_text_dict_list = list(map(search_apply_command, source_list))

    # collect all suffix
    set_suffix = set()
    for d in suffix_text_dict_list:
        set_suffix |= d.keys()
    set_suffix.remove(ORIG_CMD_STRIP)

    # replace source, per suffix, where necessary
    suffix_json_dict = {suffix: deepcopy(json_dict) for suffix in set_suffix}
    for cell_idx, suffix_text_dict in \
            reversed(list(enumerate(suffix_text_dict_list))):
        for suffix in set_suffix:

            if suffix in suffix_text_dict:
                # some command was applied to this suffix
                cell_text = suffix_text_dict[suffix]
            else:
                # not command applied ot this suffix, strip commands in output
                cell_text = suffix_text_dict[ORIG_CMD_STRIP]

            if cell_text is None:
                # delete cell
                suffix_json_dict[suffix]['cells'].pop(cell_idx)
                continue

            # source format: list of strings, each item is a line.  somehow
            # has newlines at end of each string too
            source = [_s + '\n' for _s in cell_text.split('\n')]

            # replace source
            suffix_json_dict[suffix]['cells'][cell_idx]['source'] = source

    return suffix_json_dict


def json_from_ipynb(file):
    file = pathlib.Path(file)

    with open(str(file), 'r') as f:
        return json.load(f)


def json_to_ipynb(json_dict, file):
    with open(str(file), 'w') as f:
        json.dump(json_dict, f)
