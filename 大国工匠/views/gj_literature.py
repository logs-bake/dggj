from flask import Blueprint, render_template

from models.literature_models import Literature
from utils.load_data import load_data_from_json_file

literature = Blueprint('literature', __name__, url_prefix='/literature')  # 创建名为“literature”的蓝图


@literature.route('/literature_list')
def lit_list_page():
    target_file = r"static/jsons/gj_literature.json"

    lit_list = load_data_from_json_file(target=target_file)

    # 利用render_template方法，将相关数据渲染到模板文件中
    return render_template("/literature/gj_literature_list.html", lit_list=lit_list)


@literature.route('/literature_detail/<lid>/<fname>')
def lit_detail_page(lid, fname):
    print(f"{lid=},{fname=}")
    target_file = r"static/jsons/literature/" + fname
    literature_detail = load_data_from_json_file(target=target_file)

    if literature_detail and literature_detail[0]['literature_id'] == lid:
        lit = Literature(**literature_detail[0])
    else:
        lit = None

    # 将lit和literature传递给模板文件
    return render_template("/literature/gj_literature_detail.html", literature=lit)#, literature=literature
