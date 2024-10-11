import json
import os
import re


def load_data_from_json_file(target, project_name=None):
    if not project_name:
        project_name = '大国工匠'
    base_path = os.getcwd().split(project_name)[0]
    fpath = os.path.join(base_path, project_name, target)
    if os.path.exists(fpath):
        with open(fpath, mode='r', encoding='utf-8-sig') as fp:
            infos = json.load(fp=fp)
            if isinstance(infos, dict):
                infos = [infos]
            results = []
            for info in infos:
                temp = {}
                for key, value in info.items():
                    temp[to_snake_case(key)] = value
                results.append(temp)
            return results
    else:
        return None


def to_snake_case(name):
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()



