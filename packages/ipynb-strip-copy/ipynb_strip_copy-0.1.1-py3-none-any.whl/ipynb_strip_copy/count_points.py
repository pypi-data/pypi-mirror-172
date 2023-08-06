import re

def count_points_from_json(json_dict):
    # keys are problem names, values are points
    pts_dict = dict()

    cell_list = json_dict['cells']
    for cell_dict in cell_list:
        if cell_dict['cell_type'] != 'markdown':
            continue

        for line in cell_dict['source']:
            match = re.search(r'(part|problem).+\(\d+ *(points|pts)[^\(]*\)',
                              line.lower())
            if not match:
                # no match on this line
                continue

            # break into pts and name of problem
            line = match.group()
            pts = int(line.split('(')[-1].split('p')[0])
            name = '('.join(line.split('(')[:-1]).strip()

            # store
            if name in pts_dict:
                if pts != pts_dict[name]:
                    raise AttributeError(f'multiple pt values for {name}')
            else:
                pts_dict[name] = pts

    return pts_dict


if __name__ == '__main__':
    import pathlib
    from file_ipynb import json_from_ipynb

    folder = pathlib.Path('.').resolve()
    f_ipynb = folder.parent / 'test' / 'test_case_points.ipynb'

    json_dict = json_from_ipynb(f_ipynb)

    pts_dict = count_points_from_json(json_dict)

    # stop oct 19 @ 930, riva just put eli to bed.  goal: count points and
    # print total

