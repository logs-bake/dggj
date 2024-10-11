import json
import os
from flask import Blueprint, render_template

from models.hero_models import Hero
from utils.load_data import load_data_from_json_file

hero = Blueprint('hero', __name__, url_prefix='/hero')  # 创建名为“hero”的蓝图


@hero.route('/hero_list')
def hero_list_page():
    # 利用render_template方法，将相关数据渲染到模板文件中
    target_file = r"static/jsons/gj_hero.json"

    hero_list = load_data_from_json_file(target=target_file)
    return render_template("/hero/gj_hero_list.html", hero_list=hero_list)


@hero.route('/hero_detail/<hero>/<fname>')#
def hero_detail_page(hero, fname):#

    # target_file = r"static\jsons\hero\hero_guowenchang.json"
    # hero_detail = load_data_from_json_file(target=target_file)
    # he = Hero(**hero_detail[0])
    #
    # return render_template("/hero/cz_hero_detail.html",hero=he)
    target_file = r"static/jsons/hero/" + fname

    hero_detail = load_data_from_json_file(target=target_file)

    if hero_detail and hero_detail[0]['hero_id'] == hero:
        he = Hero(**hero_detail[0])
    else:
        he= None

    return render_template("/hero/gj_hero_detail.html", hero=he)

