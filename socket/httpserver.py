#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

HOST, PORT = '', 23333


def server_run():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port %s ...' % PORT)
    while True:
        # 接受连接
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)


def handle_request(client_connection):
    # 获取请求报文
    request = ''
    while True:
        recv_data = client_connection.recv(2400)
        recv_data = recv_data.decode()
        request += recv_data
        if len(recv_data) < 2400:
            break

    # 解析首行
    first_line_array = request.split('\r\n')[0].split(' ')
    print('uri长度: %s' % len(first_line_array[1]))

    # 分离 header 和 body
    space_line_index = request.index('\r\n\r\n')
    header = request[0: space_line_index]
    body = request[space_line_index + 4:]

    # 打印请求报文
    print(request)

    # 返回报文
    http_response = b"""\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
    <head><title>Hello, World!</title></head>
    <body><p style="color: green">Hello, World!</p></body>
</html>
"""
    client_connection.sendall(http_response)
    client_connection.close()


if __name__ == '__main__':
    server_run()