# Quark
![chat](https://github.com/user-attachments/assets/c9bbe4cd-75e9-409d-9882-19db183de364)
## How does this work?
Clients communicate with each other through the server using RSA encrypted sockets with unique keys on the client side. So, server knows your username, but all messages are encrypted from client to client with AES-GCM and server can not read them. To register on server you need to get authentification code from admin(see it in config as reg_code).

## Getting started
### How to deploy a server?
```
git clone https://github.com/taldar1m/Quark-server && cd Quark-server && pip install cryptography
```
Then edit the config and run MainService.py. Now you can share your registration code with others.
### How to install the client?
![setup](https://github.com/user-attachments/assets/fe8ebfb0-8d9d-487c-b0f9-c023dc54133d)
```
git clone https://github.com/taldar1m/Quark && cd Quark && python setup.py
```
You can also download binary files of setup and main client in the releases tab.
If you don't have an account on the server, you will be registered automatically. Authentification code is reg_code from the server config. Administrator needs to provide it to all clients. Encryption passphrase is a password that will be used to encrypt local files.<br>
![decrypt](https://github.com/user-attachments/assets/91cd07ef-1bc7-4907-bfb9-36f8124d7278)
<br>To create new chat room, press "add new chat" and leave the "room key" field blank. To enter existing room, press "add new chat" and enter room key provided to you by the room's member.
