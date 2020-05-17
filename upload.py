import os


def send(file_name, connection):  # send files to client
    connection.sendall('send\n'.encode('UTF-8'))  # alert client
    print('sent')
    i = file_name.rfind('/')  # find index of last / in file destination
    connection.sendall(file_name[i+1:].encode('UTF-8'))  # send filename without the destination
    connection.recv(1)  # wait for ack

    totalbytes = os.path.getsize(file_name)
    connection.sendall(str(totalbytes).encode('UTF-8'))
    response = connection.recv(1).decode('UTF-8')  # wait for ack

    if response == 'K':
        file = open(file_name, 'rb')  # opens file and reads it in byte form
        buffer = file.read(2048)  # read 2048 bytes from file to buffer
        while buffer:
            connection.sendall(buffer)
            buffer = file.read(2048)  # read next 2048 bytes
            print("sending......", buffer)
        file.close()
    response = connection.recv(1).decode('UTF-8')
    if response == 'K':
        print('File uploaded successfully')


def download(file_path, connection):  # upload files from client to server
    #  figures out file name in windows path
    file_name = (file_path[file_path.rfind('\\')+1:])

    connection.sendall('download\n'.encode('UTF-8'))

    connection.sendall(file_path.encode('UTF-8'))  # alert client to wanted file
    response = connection.recv(1).decode('UTF-8')  # wait for client ack

    # correct ack if file found
    if response == 'K':
        file_size = connection.recv(8).decode('UTF-8')
        print('file size: ', file_size)




