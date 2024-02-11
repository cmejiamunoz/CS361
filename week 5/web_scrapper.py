# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: TCP server with web scrapping capability
# Date: Feb 10, 2024

import requests
from bs4 import BeautifulSoup
import socket
import pickle
import sys

def ski_data_request(state):
    r = requests.get(f'https://www.onthesnow.com/{state}/skireport')
    if r.status_code == 200:
        print("Site request successful.")
    else:
        print(f"Request status: {r.status_code}, {r.reason}")

    ski_info = {}
    temp_list = []
    counter = 0
    soup = BeautifulSoup(r.content,'html.parser')
    for item in soup.findAll(class_='h4 styles_h4__1nbGO'):
        if counter == 0:
            current_key = item.contents[0].lower()
            ski_info[item.contents[0].lower()] = []
            temp_list = []
            counter = 4
        elif counter == 1:
            temp_list.append(item.contents[0])
            ski_info[current_key.lower()] = temp_list
            counter -= 1
        else:
            temp_list.append(item.contents[0])
            counter -= 1
    print(f"Request complete : {ski_info}")
    return ski_info
def tcp_server_two():
    """
    Functions creates a TPC/IP socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = '127.0.0.1'
    server_port = 256
    server_socket.bind((server_address, server_port))

    server_socket.listen(5) # max number of connections before rejecting any additional.
    print("Server ready and waiting for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address}")

            try:
                message_two = client_socket.recv(4096)
                print(f'Received message: {message_two.decode()}')

                decoded_message = message_two.decode()
                dict_ski = ski_data_request(decoded_message)
                sys.setrecursionlimit(30000)                                # increased the limit of recusrion to allow data to be pickled.
                json_dict = pickle.dumps(dict_ski,-1)                       # converted dictionary to byte data in order to allow it to be sent via sockets.


                client_socket.sendall(json_dict)
            finally:
                client_socket.close()
                print(f'Connection with {client_address} closed')
    except KeyboardInterrupt:
        print("Server is shutting down..")
    finally:
        server_socket.close()
        print("Server socket is now closed.")

if __name__ == '__main__':
    tcp_server_two()

