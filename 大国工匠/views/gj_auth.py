import json
import os
import re
import uuid

from flask import Blueprint, render_template, request, session, flash, url_for, redirect, current_app, g
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models.global_data import SECRET_KEY

auth = Blueprint('auth', __name__, url_prefix='/auth')

db = MongoClient().db_cz
users_collection = db.users

# 初始化URLSafeTimedSerializer对象，用于生成和验证令牌
ts = URLSafeTimedSerializer(SECRET_KEY)

user_reg = r'^[\u4e00-\u9fa5a-zA-Z0-9_-]{5,20}$'
pass_reg = r'^(?![\d]+$)(?![a-z]+$)(?![A-Z]+$)(?![!#$%^&*]+$)[\da-zA-z!#$%^&*]{8,20}$'
email_reg = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # 实现用户登录的相关处理
        username = request.form['username']
        password = request.form['password']
        # 判断用户名是否是 5-20 个字符
        if not re.match(user_reg, username):
            return render_template("/auths/gj_login.html", account_errmsg='请输入正确的用户名！')
        # 判断密码是否是 8-20 位的字母，数字和特殊字符的二种以上
        if not re.match(pass_reg, password):
            return render_template("/auths/gj_login.html",
                                   account_errmsg='密码长度必须为 8 ~ 20 位，并包含字母、数字、特殊字符的二种以上！！')
        user_in_db = users_collection.find_one({'username': username})
        if not user_in_db or not check_password_hash(user_in_db['password_hash'], password):
            return render_template("/auths/gj_login.html", account_errmsg='用户名或密码错误！')
        session['cz_token'] = ts.dumps(username)  # 生成令牌并保存到会话中
        session['username'] = username  # 保存用户名到会话，以便于在根模板上展示用户登录信息
        return redirect(url_for('main'))
    else:
        # 利用render_template方法，将相关数据渲染到模板文件中
        return render_template("/auths/gj_login.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # 获取注册信息
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        mobile = request.form['mobile']
        email = request.form['email']
        file = request.files['avatar']
        # file = request.files['head_img']
        # 校验参数合法性
        if not all([username, password, password2, mobile]):  # 校验必填的参数
            return render_template("/auths/gj_register.html", register_errmsg='请填写所有注册项！')
        if not re.match(user_reg, username):  # 判断用户名是否是5-20个字符
            return render_template("/auths/gj_register.html", register_errmsg='请输入5-20个字符的用户名！')
        if not re.match(r'^1[3-9]\d{9}$', mobile):  # 判断手机号码是否合法
            return render_template("/auths/gj_register.html", register_errmsg='请输入正确的手机号码！')
        if not re.match(email_reg, email):  # 判断邮箱地址是否合法
            return render_template("/auths/gj_register.html", register_errmsg='请输入正确的邮箱地址！')
        if not re.match(pass_reg, password):  # 判断密码是否是8-20个字符
            return render_template("/auths/gj_register.html",
                                   register_errmsg='请输入8-20位的密码，并包含字母、数字、特殊字符的二种以上！')
        if password != password2:  # 判断两次输入的密码是否相同
            return render_template("/auths/gj_register.html", register_errmsg='两次输入的密码不一致！')
        user_in_db = users_collection.find_one({'username': username})  # 判断用户名是否已被使用
        if user_in_db:
            return render_template("/auths/gj_register.html", register_errmsg='用户名已被使用，请使用其他用户名注册！')
        avatar_path = 'images/gj1.jpg'   # 默认用户头像的保存路径


        if file and allowed_file(file.filename):    # 保存用户上传的头像
            # 生成唯一的文件名称标识符
            file_id = str(uuid.uuid4())
            # 获取原始文件名和扩展名
            original_filename = secure_filename(file.filename)
            filename, ext = os.path.splitext(original_filename)
            # 构建新的文件名，包括唯一标识符和原始扩展名
            new_filename = f"{file_id}{ext}"
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
            # 保存文件到指定目录
            file.save(os.path.join(os.getcwd(), "static", avatar_path))
        new_user = {   # 构建用户信息
            'username': username,
            'mobile': mobile,
            'email': email,
            'avatar': avatar_path,
            'password_hash': generate_password_hash(password)
         }
        users_collection.insert_one(new_user)   # 保存用户信息到数据库中
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    else:
        # 利用render_template方法，将相关数据渲染到模板文件中
        return render_template("/auths/gj_register.html")


@auth.route('/modify', methods=['POST', 'GET'])
def modify_info():
    if request.method == 'POST':
        # 实现用户信息修改的相关处理
        pass
    else:
        # 利用render_template方法，将相关数据渲染到模板文件中
        return render_template("/auths/gj_modify_info.html")


@auth.route('/logout')
def logout():
    # 移除会话中的令牌
    if 'cz_token' in session:
        session.pop('cz_token')
        session.pop('username')
    flash('已注销登录')
    return redirect(url_for('main'))


@auth.before_app_request
def verify_token():
    # 指定某些请求的路由需要进行安全认证才可以访问
    if request.endpoint not in ['forum.submit_comment', 'cart', 'chat.cz_chat']:
        return

    if 'cz_token' not in session:
        return redirect(url_for('auth.login'))
    try:
        username = ts.loads(session['cz_token'], max_age=current_app.config['PERMANENT_SESSION_LIFETIME'])
    except SignatureExpired:
        return redirect(url_for('auth.login'))
    user_in_db = users_collection.find_one({'username': username})
    if not user_in_db:
        return redirect(url_for('auth.login'))
    # 将用户对象添加到g变量中，以便视图中使用
    g.user = user_in_db