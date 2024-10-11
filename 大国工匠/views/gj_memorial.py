import json
import os
from flask import Blueprint, render_template

from models.memorial_models import Memorial
from utils.load_data import load_data_from_json_file
memorial = Blueprint('memorial', __name__, url_prefix='/memorial')  # 创建名为“memorial”的蓝图


@memorial.route('/memorial_list')
def mem_list_page():
    # 利用render_template方法，将相关数据渲染到模板文件中
    target_file = r"static/jsons/gj_memorial.json"
    memorial_list = load_data_from_json_file(target=target_file)

    return render_template("/memorial/gj_memorial_list.html", memorial_list=memorial_list)

@memorial.route('/memorial_detail/<mem>/<fname>')#
def memorial_detail_page(mem, fname):#

    target_file = r"static/jsons/memorial/" + fname

    memorial_detail = load_data_from_json_file(target=target_file)

    if memorial_detail and memorial_detail[0]['memorial_id'] == mem:
        me = Memorial(**memorial_detail[0])
    else:
        me = None

    return render_template("/memorial/gj_memorial_detail.html", memorial=me)

