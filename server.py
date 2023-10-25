import socket
import threading

host = "127.0.0.1"
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)

words = ["python", "programming", "hangman", "socket", "threading"]

def play_game(client_socket, word):
    max_attempts = 6
    attempts = 0
    guessed_letters = set()
    word_set = set(word)
    hidden_word = ["_" if letter.isalpha() else letter for letter in word]

    while attempts < max_attempts:
        guess = client_socket.recv(1024).decode().lower()

        if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            client_socket.send("Invalid guess. Try again.".encode())
            continue

        guessed_letters.add(guess)

        if guess in word_set:
            for i, letter in enumerate(word):
                if letter == guess:
                    hidden_word[i] = guess

            if set(hidden_word) == word_set:
                client_socket.send(("You win! The word was: " + word).encode())
                break
            else:
                client_socket.send(("".join(hidden_word)).encode())
        else:
            attempts += 1
            client_socket.send(f"Wrong guess ({attempts}/{max_attempts} attempts left).".encode())

    if attempts >= max_attempts:
        client_socket.send(("You lose! The word was: " + word).encode())

    client_socket.close()

def main():
    print("Server listening on {}:{}".format(host, port))
    player_num = 0

    while True:
        client_socket, client_address = server_socket.accept()
        player_num += 1
        word = words[player_num - 1] if player_num <= len(words) else "default"

        if player_num <= 2:
            client_socket.send("Welcome to Hangman! Guess a letter.".encode())
            game_thread = threading.Thread(target=play_game, args=(client_socket, word))
            game_thread.start()
        else:
            client_socket.send("Sorry, the game is full. Try again later.".encode())
            client_socket.close()

if __name__ == "__main__":
    main()
