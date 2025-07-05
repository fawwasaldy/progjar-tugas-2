import socket
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        logging.info(f"Koneksi baru dari {client_address}")

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                request = data.decode('utf-8').strip()
                logging.info(f"Menerima request: '{request}' dari {self.client_address}")

                if request.upper() == "TIME":
                    current_time = time.strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.client_socket.sendall(response.encode('utf-8'))
                    logging.info(f"Mengirim waktu '{current_time}' ke {self.client_address}")
                elif request.upper() == "QUIT":
                    break
                else:
                    response = "Perintah tidak valid. Gunakan 'TIME' atau 'QUIT'.\r\n"
                    self.client_socket.sendall(response.encode('utf-8'))
                    logging.warning(f"Perintah tidak valid dari {self.client_address}")

        except Exception as e:
            logging.error(f"Error pada koneksi dengan {self.client_address}: {e}")
        finally:
            logging.info(f"Koneksi dengan {self.client_address} ditutup.")
            self.client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('0.0.0.0', 45000)
    server_socket.bind(server_address)
    logging.info(f"Server berjalan di {server_address[0]}:{server_address[1]}")

    server_socket.listen(5)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            new_thread = ClientThread(client_socket, client_address)
            new_thread.start()
    except KeyboardInterrupt:
        logging.info("Server dihentikan.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()