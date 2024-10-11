import json
import os
from json import JSONDecodeError

from flask import Blueprint, render_template
from models.global_data import v_list
profile = Blueprint('profile', __name__)


@profile.route('/profile')
def profile_page():
    fpath = os.path.join(os.getcwd(), "static/jsons/gj_profile_data.json")

    try:
        with open(fpath, mode='r', encoding='utf-8') as fp:
            profiles = json.load(fp=fp)
            lines = []
            if profiles:
                for idx, item in enumerate(profiles["czProfileArmy"]):
                    temp = item.split(":", 1)
                    line = {
                        'army': temp[0],
                        'desc': temp[1],
                        'line_img': profiles["czProfileLinePics"][idx]
                    }
                    idx += 1
                    lines.append(line)
    except FileNotFoundError as fe:
        print(f"文件路径：{fpath} 不存在，请检查！{fe}")
        profiles = lines = None
    except JSONDecodeError as je:
        print(f"解析文件：{fpath} 出错，请检查！")
        profiles = lines = None
    except Exception as e:
        print(f"其他异常情况：{e}")
        profiles = lines = None
    # 利用render_template方法，将相关数据渲染到模板文件中
    return render_template("index/gj_profile.html", v_list=v_list, profiles=profiles, lines=lines)
