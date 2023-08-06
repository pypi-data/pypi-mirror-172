from ipynb_strip_copy import *


def test_quick():
    file_in = 'test_case.ipynb'
    file_out0 = 'test_case0.ipynb'
    file_out1 = 'test_case1.ipynb'

    json_in = json_from_ipynb(file_in)
    json_out0 = json_from_ipynb(file_out0)
    json_out1 = json_from_ipynb(file_out1)

    suffix_json_dict = search_apply_json(json_in)

    assert suffix_json_dict['0'] == json_out0
    assert suffix_json_dict['1'] == json_out1


def test_pts():
    file_in = 'test_case_points.ipynb'
    json_dict = json_from_ipynb(file_in)

    pts_dict = count_points_from_json(json_dict)

    pts_dict_expect = {'part 1': 20.0,
                       'problem 2': 13.0,
                       'part 3.398234 the quick brown fox': 15.0,
                       'part 4.2 b': 12.0}

    assert pts_dict == pts_dict_expect
