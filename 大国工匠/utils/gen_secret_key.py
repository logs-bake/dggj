import os
import base64


def generate_secret_key():
    # 从系统环境中获取随机字节
    random_bytes = os.urandom(24)
    # 使用base64编码生成字符串
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    return secret_key


secret_key = generate_secret_key()
print(secret_key)


