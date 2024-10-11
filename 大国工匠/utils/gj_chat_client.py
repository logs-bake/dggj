import socket
import threading


class ChatClient:
    def __init__(self, host='127.0.0.1', port=22222):#18888
        self.nickname = input("请输入您的用户名：")
        self.host = host  # 服务端主机地址
        self.port = port  # 服务端端口号
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP通信的套接字
        self.client.connect((self.host, self.port))  # 连接到服务端

    def receive(self):  # 接收服务端发过来的信息
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':  # 接收到的是请求提供用户名的消息
                    self.client.send(self.nickname.encode('utf-8'))
                else:  # 否则是服务端发来的聊天消息，在本地显示出来
                    print(message)
            except Exception as e:
                print(f"出错了！{e}")
                self.client.close()
                break

    def send(self):  # 向服务端发送信息
        while True:
            try:
                message = input()  # 等待用于输入要发送的信息
                if len(message) > 0:
                    self.client.send(message.encode('utf-8'))
            except Exception as e:
                print("出现异常：", e)

    def run(self):
        # 创建一个接收线程，指定处理方法是类的实例方法receive()
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  # 启动接收线程
        # 创建一个发送线程，指定处理方法是类的实例方法send()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()  # 启动发送线程


if __name__ == "__main__":
    client = ChatClient()
    client.run()
