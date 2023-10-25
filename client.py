import socket

host = "127.0.0.1"
port = 12345 

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))

    while True:
        response = client_socket.recv(1024).decode()
        print(response)

        guess = input("Your guess: ").lower()

        client_socket.send(guess.encode())

        if "win" in response or "lose" in response:
            break

    client_socket.close()

if __name__ == "__main__":
    main()