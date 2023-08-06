import warnings

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


def get_validate_rules(hocons_dir=None):
    import os
    import sys
    import json
    from spark_quality_rules_tools.utils import BASE_DIR
    from spark_quality_rules_tools.utils.color import get_color, get_color_b
    from pyhocon.converter import HOCONConverter
    from pyhocon import ConfigFactory

    is_windows = sys.platform.startswith('win')
    dir_resource_rules = os.path.join(BASE_DIR, "utils", "resource", "rules.json")

    if hocons_dir in ("", None):
        raise Exception(f'required variable hocons_dir')

    if is_windows:
        dir_resource_rules = dir_resource_rules.replace("\\", "/")
        hocons_dir = hocons_dir.replace("\\", "/")

    with open(dir_resource_rules) as f:
        parameter_conf = json.load(f)

    validate_rules_properties_columns = parameter_conf["rules_common_properties"][0]["rules_columns"]
    validate_rules_properties_datatype = parameter_conf["rules_common_properties"][0]["rules_datatype"]
    validate_rules_config = parameter_conf["rules_config"]

    dir_confs_filename_parameters2 = hocons_dir
    conf = ConfigFactory.parse_file(dir_confs_filename_parameters2)
    res = HOCONConverter.to_json(conf)
    res = json.loads(res)
    rules = res["hammurabi"]["rules"]

    for k in rules:
        hocons_rules = str(k["class"])
        hocons_config = k["config"]
        hocons_rules_type = str(hocons_rules).split(".")[4]
        hocons_rules_class = str(hocons_rules).split(".")[5]

        validate_rules_class = validate_rules_config[hocons_rules_type][hocons_rules_class]
        validate_rules_version = validate_rules_class[0]["rules_version"]
        validate_rules_columns = validate_rules_class[0]["rules_columns"]
        validate_rules_datatype = validate_rules_class[0]["rules_datatype"]

        validate_total_columns = validate_rules_properties_columns + validate_rules_columns
        validate_total_datatype = dict(**validate_rules_properties_datatype, **validate_rules_datatype)

        print("type=>", hocons_rules_type, "class=>", hocons_rules_class, "version=>", validate_rules_version)

        if 'id' not in hocons_config.keys():
            print(f"{get_color('Variable id:')} {get_color_b('No existe')}")
        else:
            print(f"{get_color('Variable id:')} {get_color_b(hocons_config['id'])}")

        for k, v in hocons_config.items():
            if not str(k) in validate_total_columns:
                print(f"{get_color('Variable Deprecada:')} {get_color_b(k)}")
            else:
                print(f"{get_color('Variable Correcta:')} {get_color_b(k)}")
        print("-------------------------------")
