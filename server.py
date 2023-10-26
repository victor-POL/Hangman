import socket
import threading
import signal
import sys
import random

host = "127.0.0.1"
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

words = ["python"]

def play_game(client_socket, word, player_id):
    max_attempts = 6
    attempts = 0
    guessed_letters = set()
    word_set = set(word)
    hidden_word = ["_" if letter.isalpha() else letter for letter in word]

    try:
        while attempts < max_attempts:
            guess = client_socket.recv(1024).decode().lower()
            response = ""

            if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
                response = "Invalid guess. Try again."
                continue

            guessed_letters.add(guess)

            if guess in word_set:
                for i, letter in enumerate(word):
                    if letter == guess:
                        hidden_word[i] = guess

                if set(hidden_word) == word_set:
                    client_socket.send(("You win ! The word was: " + word).encode())
                    break
                else:
                    response = "".join(hidden_word)
            else:
                attempts += 1
                response = "Wrong guess (" + str(max_attempts - attempts) + " attempts left)."
            client_socket.send(response.encode())

        if attempts == max_attempts:
            client_socket.send(("You lose ! The word was: " + word).encode())
    except ConnectionError:
        pass
    finally:
        print("Player " + str(player_id) + " disconnected")
        client_socket.close()

def signal_handler(sig, frame):
    print('Close server')
    server_socket.close()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Server listening on {}:{}".format(host, port))
    player_num = 0

    while True:
        client_socket, client_address = server_socket.accept()
        player_num += 1
        word = words[random.randint(0, len(words)-1)]

        print("Player " + str(player_num) + " connected")
        game_thread = threading.Thread(target=play_game, args=(client_socket, word, player_num))
        game_thread.start()

if __name__ == "__main__":
    main()

