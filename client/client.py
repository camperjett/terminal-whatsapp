import threading
import socket
import sys

HOST ='127.0.0.1'
PORT =8081
BUFFER=4096



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  client.connect((HOST,PORT))
  nickname= input("Enter a new username: ")

  if nickname=="admin":
    password= input("Enter Password: ")
except:
  sys.exit('Server is currently offline')

stop_thread = False

def recieve():
  while True:
    global stop_thread
    if stop_thread:
      break 
    try:
      msg= client.recv(BUFFER).decode('utf-8')
      if msg == ">USER":
        
        client.send(nickname.encode('utf-8'))
        server_msg= client.recv(BUFFER).decode('utf-8')

        if server_msg == ">ADMINPASS":
          client.send(password.encode('utf-8'))
          if client.recv(BUFFER).decode('utf-8') == '>WRONG_ADMINPASS':
            print("Connection refused: wrong password")
            stop_thread=True
        elif server_msg == ">BANNED":
          print("Connection refused: banned username")
          client.close()
          stop_thread=True
          break
        elif server_msg == ">DUPLICATE":
          print("User already in use")
          client.close()
          stop_thread=True
          break
      else:
        print(msg)
    except:
      print("Error occured")
      client.close()
      break

def write():
  while True:
    msg = f'{nickname}: {input("")}'
    if msg[len(nickname)+2:].startswith('/'):
      if nickname=='admin':
        if msg[len(nickname)+2:].startswith('/kick'):
          client.send(f"/KICK {msg[len(nickname)+2+6:]}".encode('utf-8'))
        elif msg[len(nickname)+2:].startswith('/ban'):
          client.send(f"/BAN {msg[len(nickname)+2+5:]}".encode('utf-8'))
      else:
        print("Command can be executed only by admin")
    else:
      client.send(msg.encode('utf-8'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
