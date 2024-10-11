import json
from urllib import request

from flask import Blueprint, render_template, current_app, session, redirect, url_for, jsonify
from flask_socketio import emit
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymongo import MongoClient

from models.global_data import SECRET_KEY

chat = Blueprint('chat', __name__, url_prefix='/chat')  # 创建名为”chat“的蓝图

clients = []
# 初始化URLSafeTimedSerializer对象，用于生成和验证令牌
ts = URLSafeTimedSerializer(SECRET_KEY)

db = MongoClient().db_cz
users_collection = db.users


@chat.route("/")
def cz_chat():  # 处理聊天页面请求的视图函数
    try:
        # 查看用户是否已登录
        username = ts.loads(session['cz_token'], max_age=current_app.config['PERMANENT_SESSION_LIFETIME'])
    except Exception:
        # except SignatureExpired:
        return redirect(url_for('auth.login'))
    user_in_db = users_collection.find_one({'username': username})
    if not user_in_db:
        return redirect(url_for('auth.login'))
    # 用户已登录，利用render_template方法，渲染模板文件，并将用户信息传递到模板文件中
    return render_template("gj_chat.html", user={'username': user_in_db['username'],
                                                 'userid': str(user_in_db['_id']), "avatar": user_in_db['avatar']})


@chat.route('/join', methods=['POST'])
def join():
    data = request.get_json()
    client_id = len(clients)
    clients.append(data)
    emit(current_app, 'message', f'用户 {client_id} 加入了聊天室.\n', (client_id, client_id))
    return jsonify({'client_id': client_id}), 201


@chat.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    client_id = data['client_id']
    message = data['message']
    emit('message', f'{client_id}: {message}\n', (client_id))
    return ''


def emit(app, event, message, clients):
    for client in clients:
        if client not in clients:
            continue
        app.send_packet(client, json.dumps({'event': event, 'message': message}))
