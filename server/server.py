import threading
import socket

HOST ='localhost'
PORT ='8080'

server = socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
