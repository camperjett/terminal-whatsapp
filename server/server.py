import threading
import socket

HOST ='127.0.0.1'
PORT =8084
BUFFER = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients= []
nicknames=[]

def broadcast(msg):
  for client in clients:
    client.send(msg)

def handle(client):
  while True:
    try:
      msg=client.recv(BUFFER)
      broadcast(msg)
    except:
      index = clients.index(client)
      clients.remove(client)
      client.close()

      nickname = nicknames[index]
      nicknames.remove(nickname)

      broadcast(f"\n{nickname} left the chat\n".encode('utf-8'))
      break

def receive():
  while True:
    client, address=server.accept()

    client.send("\1".encode('utf-8'))
    nickname=client.recv(BUFFER).decode('utf-8')
    #   ISSUE(7) solved
    # if nickname in nicknames:
    #   while nickname in nicknames:
    #     client.send("What should we call you: ".encode('utf-8'))
    #     nickname=client.recv(BUFFER).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)
    print(f"{str(address)} connected to server as {nickname}")
    broadcast(f"\n{nickname} has joined the chat\n".encode('utf-8'))
    client.send("\nConnected to Server\n".encode('utf-8'))

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

print(f"Server is Up and listening on {HOST}:{PORT}")
receive()
