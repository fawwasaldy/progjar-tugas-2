import socket

server_address = ('127.0.0.1', 45000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(server_address)
    print("Terhubung ke server.")

    request = "TIME\r\n"
    client_socket.sendall(request.encode('utf-8'))
    print(f"Mengirim request: {request.strip()}")

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Menerima respons: {response.strip()}")

    request = "QUIT\r\n"
    client_socket.sendall(request.encode('utf-8'))
    print(f"Mengirim request: {request.strip()}")

except Exception as e:
    print(f"Error: {e}")
finally:
    print("Menutup koneksi.")
    client_socket.close()