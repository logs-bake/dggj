from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from models.global_data import *

from views.gj_profile import profile
from views.gj_auth import auth
from views.gj_history import history
from views.gj_hero import hero
from views.gj_video import video
from views.gj_battle import battle
from views.gj_literature import literature
from views.gj_memorial import memorial
from views.gj_chat import chat

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGODB_URI'] = 'mongodb://localhost:27017/db_gj'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 设置会话过期时间为1小时
app.config['UPLOAD_FOLDER'] = 'images/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 将可能的蓝图路由封装到元组中，以便于下面通过for循环将多个蓝图注册到主应用上
bps = (profile, auth, history, hero, video, battle, literature, memorial, chat)
for bp in bps:
    app.register_blueprint(bp)  # 将对应的路由实现蓝图注册到主app应用上

context = {
    "v_list": v_list,
    "info_list": gj_infos.split("\n"),
    "gj_leader": gj_leader,
    "gj_stage": gj_stage,
    "gj_navs": gj_navs
}


@app.route("/")
def main():
    return render_template("/index/gj_index.html", **context)


# 实例化一个SocketIO对象
socketio = SocketIO(app, cors_allowed_origins="*")


# 聊天消息处理方法，此处只是简单的将消息广播给所有在线的客户端
@socketio.on('message')
def handle_message(message):
    print(f"{message=}")
    emit('message', message, broadcast=True)


# 客户端新建连接请求的处理方法，将用户进入聊天室的消息广播给所有在线的客户端
@socketio.on('user_info')
def handle_connect(user_info):
    emit('welcome', {'text': "欢迎" + user_info['username'] + "加入聊天室"}, broadcast=True)


if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    # app.run(port=19999, host="0.0.0.0", debug=True)
    socketio.run(app, port=22222, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)  # 换成使用SocketIO的实例对象启动主应用allow_unsafe_werkzeug=True
    # socketio.run(app, port=22222,allow_unsafe_werkzeug=True)