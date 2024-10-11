import json
import os
from flask import Blueprint, render_template
from models.history_models import History
from utils.get_comments_from_douban import get_comments
from utils.load_data import load_data_from_json_file

history = Blueprint('history', __name__, url_prefix='/history')  # 创建名为“history”的蓝图


@history.route('/history_list')
def history_list_page():
    target_file = r"static/jsons/gj_history.json"
    history_list = load_data_from_json_file(target=target_file)
    # print(history_list)
    # 利用render_template方法，将相关数据渲染到模板文件中
    return render_template("/history/gj_his_list.html", his_list=history_list)


@history.route('/history_detail/<his>/<fname>')
def history_detail_page(his, fname):

    # target_file = r"static\jsons\history\vid_changzheng_ds.json"
    # history_detail = load_data_from_json_file(target=target_file)
    # vd = history(**history_detail[0])
    #
    # return render_template("/history/cz_history_detail.html",history=vd)

    target_file = r"static/jsons/history/" + fname

    history_detail = load_data_from_json_file(target=target_file)
    print('id',history_detail)
    print("his",his)

    if history_detail and history_detail[0]['history_id'] == his:
        hs = History(**history_detail[0])

        if his == 'v00100001':
            urls = [
                "https://movie.douban.com/subject/26910902/reviews?sort=time"
            ]
            temp = []
            for url in urls:
                result = get_comments(url)
                temp.extend(result)
            hs.comments = temp
    else:
        hs = None
    print("hs",hs)

    return render_template("/history/gj_history_detail.html", history=hs)