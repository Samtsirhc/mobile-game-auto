import socket
import string
# 建立一个服务端

def run_task(task): 
    if check_task(task):
        return f'执行 {task}'
    else:
        return f'任务 {task} 不存在'

def check_task(task):
    return True


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',6999)) #绑定要监听的端口
    server.listen(5) #开始监听 表示可以使用五个链接排队

    while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
        conn,addr = server.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
        print(conn,addr)
        while True:
            try:
                data = conn.recv(1024).decode()  #接收数据
                res = run_task(data)
                conn.send(res.encode()) #然后再发送数据
            except ConnectionResetError as e:
                print('关闭了正在占线的链接！')
                break
        conn.close()


