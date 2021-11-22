import threading
import socket
import sys

HOST ='127.0.0.1'
PORT =8084
BUFFER=4096



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  client.connect((HOST,PORT))
  nickname= input("Enter a new username: ")
except:
  sys.exit('Server is currently offline')


def recieve():
  while True:
    try:
      msg= client.recv(BUFFER).decode('utf-8')
      if msg == "\1":
        
        client.send(nickname.encode('utf-8'))
      else:
        print(msg)
    except:
      print("Error occured")
      client.close()
      break

def write():
  while True:
    msg = f'{nickname}: {input("")}'.encode('utf-8')
    client.send(msg)

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
