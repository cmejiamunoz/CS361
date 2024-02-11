# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: TCP server with integrated weather API.
# Date: Feb 04, 2024.

import socket
import python_weather
import asyncio

async def weather_data(city):
   async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
       weather_info = await client.get(city)
   return weather_info.current.temperature

def tcp_server():
    """
    Functions creates a TPC/IP socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = '127.0.0.1'
    server_port = 255
    server_socket.bind((server_address, server_port))

    server_socket.listen(5) # max number of connections before rejecting any additional.
    print("Server ready and waiting for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address}")

            try:
                message = client_socket.recv(1024)
                print(f'Received message: {message.decode()}')

                decoded_message = message.decode()
                weather_info = str(asyncio.run(weather_data(decoded_message)))

                client_socket.sendall(weather_info.encode())
            finally:
                client_socket.close()
                print(f'Connection with {client_address} closed')
    except KeyboardInterrupt:
        print("Server is shutting down..")
    finally:
        server_socket.close()
        print("Server socket is now closed.")

if __name__ == '__main__':
    tcp_server()