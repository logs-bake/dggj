import json
import os
from flask import Blueprint, render_template

from models.battle_models import Battle

from utils.load_data import load_data_from_json_file

battle = Blueprint('battle', __name__, url_prefix='/battle')  # 创建名为“battle”的蓝图


@battle.route('/battle_list')
def bat_list_page():
    # 利用render_template方法，将相关数据渲染到模板文件中
    target_file = r"static/jsons/gj_battle.json"

    battle_list = load_data_from_json_file(target=target_file)
    return render_template("/battle/gj_battle_list.html", battle_list=battle_list)

@battle.route('/battle_detail/<bat>/<fname>')#
def battle_detail_page(bat, fname):#

    target_file = r"static/jsons/battle/" + fname

    battle_detail = load_data_from_json_file(target=target_file)

    if battle_detail and battle_detail[0]['battle_id'] == bat:
        ba = Battle(**battle_detail[0])
    else:
        ba = None

    return render_template("/battle/gj_battle_detail.html", battle=ba)


