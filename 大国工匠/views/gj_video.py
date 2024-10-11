import json
import os
from flask import Blueprint, render_template
#
from models.video_models import Video
from utils.get_comments_from_douban import get_comments
from utils.load_data import load_data_from_json_file

video = Blueprint('video', __name__, url_prefix='/video')  # 创建名为“video”的蓝图


@video.route('/video_list')
def video_list_page():
    target_file = r"static/jsons/gj_video.json"
    video_list = load_data_from_json_file(target=target_file)
    # 利用render_template方法，将相关数据渲染到模板文件中
    return render_template("/video/gj_video_list.html", video_list=video_list)


@video.route('/video_detail/<vid>/<fname>')
def video_detail_page(vid, fname):

    # target_file = r"static\jsons\video\vid_changzheng_ds.json"
    # video_detail = load_data_from_json_file(target=target_file)
    # vd = Video(**video_detail[0])
    #
    # return render_template("/video/cz_video_detail.html",video=vd)

    target_file = r"static/jsons/video/" + fname

    video_detail = load_data_from_json_file(target=target_file)

    if video_detail and video_detail[0]['video_id'] == vid:
        vd = Video(**video_detail[0])
        if vid == 'v00100001':
            urls = [
                "https://movie.douban.com/subject/26910902/reviews?sort=time"
            ]
            temp = []
            for url in urls:
                result = get_comments(url)
                temp.extend(result)
            vd.comments = temp
    else:
        vd = None

    return render_template("/video/gj_video_detail.html", video=vd)