from app.detection import ml_utils
import json


# Test dictionary conversion
def test_convert_dict_to_json():
    my_dict = {'scores': [1, 2, 3]}
    my_list_gt = json.dumps({'scores': [1, 2, 3]})
    my_list = ml_utils.convert_dict_to_json(my_dict)
    assert my_list == my_list_gt
