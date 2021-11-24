import threading
import socket

HOST ='127.0.0.1'
PORT =8081
BUFFER = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients= []
nicknames=[]


def kick_user(user):
  if user != "admin":
    if user in nicknames:
      name_index= nicknames.index(user)
      client_to_kick= clients[name_index]
      clients.remove(client_to_kick)
      client_to_kick.send('You were kicked by admin'.encode('utf-8'))
      client_to_kick.close()
      nicknames.remove(user)
      broadcast(f"{user} was kicked by admin".encode('utf-8'))
    else:
      print(f"\n{user} doesnt exist")
    


def ban_user(user):
  if user != "admin":
    kick_user(user)
    with open('banned.txt', 'a') as f:
      f.write(f'{user}\n')
    print(f"{user} is banned!")


def broadcast(msg):
  for client in clients:
    client.send(msg)

def handle(client):
  while True:
    try:
      message = msg=client.recv(BUFFER)
      if message.decode('utf-8').startswith('/'):
        if nicknames[clients.index(client)] == 'admin':
          if message.decode('utf-8').startswith('/BAN'):
            name_to_kick= message.decode('utf-8')[5:]
            ban_user(name_to_kick)
          if message.decode('utf-8').startswith('/KICK'):
            name_to_ban= message.decode('utf-8')[6:]
            kick_user(name_to_ban)
        else:
          client.send('Command refused')
      else:
        broadcast(msg)
    except:
      if client in clients:
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

    client.send(">USER".encode('utf-8'))
    nickname=client.recv(BUFFER).decode('utf-8')
    #   ISSUE(7) solved
    # if nickname in nicknames:
    #   while nickname in nicknames:
    #     client.send("What should we call you: ".encode('utf-8'))
    #     nickname=client.recv(BUFFER).decode('utf-8')

    with open('banned.txt', 'r') as f:
      bans = f.readlines()

    if nickname+'\n' in bans:
      client.send('>BANNED'.encode('utf-8'))
      client.close()
      continue

    if nickname == "admin":
      client.send(">ADMINPASS".encode('utf-8'))
      password = client.recv(BUFFER).decode('utf-8')
      if password != "12345":
        client.send('>WRONG_ADMINPASS'.encode('utf-8'))
        client.close()  
        continue

    if nickname in nicknames:
      client.send(">DUPLICATE".encode('utf-8'))
    else:
      nicknames.append(nickname)
      clients.append(client)

    print(f"{str(address)} connected to server as {nickname}")
    broadcast(f"\n{nickname} has joined the chat\n".encode('utf-8'))
    
    client.send("\nConnected to Server\n".encode('utf-8'))

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

print(f"Server is Up and listening on {HOST}:{PORT}")
receive()
