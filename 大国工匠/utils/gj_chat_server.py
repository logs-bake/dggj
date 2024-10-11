import socket
import threading


# 定义一个聊天室的服务类
class ChatServer:
    def __init__(self, host='127.0.0.1', port=22222):#18888
        """ 聊天室服务类的构造方法，可指定主机地址及端口号"""
        self.host = host  # 主机地址
        self.port = port  # 端口号
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建IPV4格式的TCP通信服务端套接字
        self.server.bind((self.host, self.port))  # 绑定到指定的IP及端口号上
        self.server.listen()  # 启动服务器，监听客户端连接请求
        print(f"聊天室服务端已启动，正在等待客户连接请求的到来......")
        self.clients = []  # 初始化客户端列表，每个列表元素为一个二元组：（客户端套接字对象，客户端用户昵称）

    # 向所有在线用户广播发送消息的方法
    def broadcast(self, message):
        for client in self.clients:  # 逐一向当前在线的聊天用户发送消息
            try:
                client['skt'].send(message)
            except Exception as e:
                print(e)
                print(f'{client["nickname"]} 离开了聊天室.\n')

    # 服务端输入并发送消息给所有客户端的方法
    def service_send(self):
        while True:
            try:
                message = input()
                if len(message) > 0:
                    self.broadcast(("客服回复： " + message).encode('utf-8'))
            except Exception as e:
                print("出现异常：", e)

    # 定义对客户端发送过来的消息的处理方法
    def handle(self, client):
        while True:
            try:
                message = client['skt'].recv(1024)
                if message:
                    print(f'{client["nickname"]}: {message.decode("utf-8")}')  # 在服务端中显示消息
                    self.broadcast(f'{client["nickname"]}: {message.decode("utf-8")}'.encode('utf-8'))  # 将消息广播出去
                else:
                    break
            except Exception as e:
                print(e)
                self.broadcast(f'{client["nickname"]} 离开了聊天室.\n'.encode('utf-8'))
                break

    def receive(self):
        while True:
            skt, address = self.server.accept()
            print(f"{str(address)} 建立会话连接...")

            skt.send('NICK'.encode('utf-8'))  # 要求客户端提供用户名
            nickname = skt.recv(1024).decode('utf-8')
            client = {'skt': skt, 'nickname': nickname}  # 构建客户端信息的字典结构
            self.clients.append(client)  # 将新的客户端加入到客户端列表中

            print(f"{nickname} 进入聊天室 !")
            self.broadcast(f"{nickname} 进入聊天室 !".encode('utf-8'))

            # 创建一共客户端消息处理线程，指定处理方法是类的实例方法handle()，并传入客户端字典对象，以便为每一个客户端建立一个socket连接
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()  # 启动·客户端消息处理线程

            # 创建一个服务端消息发送线程，指定处理方法是类的实例方法service_send()
            send_thread = threading.Thread(target=self.service_send)
            send_thread.start()  # 启动服务端消息发送线程


if __name__ == "__main__":
    server = ChatServer()
    server.receive()
