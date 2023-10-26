import signal
import sys
import socket
import curses
from curses import wrapper

host = "127.0.0.1"
port = 12345 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def signal_handler(sig, frame):
    print('Close client')
    client_socket.close()
    sys.exit(0)

def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)

    client_socket.connect((host, port))

    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Hangman! Guess a letter.")
    stdscr.addstr(1, 0, "Input letter: ")
    stdscr.refresh()

    while True:
        guess = chr(stdscr.getch()).lower()

        client_socket.send(guess.encode())

        response = client_socket.recv(1024).decode()

        if "Invalid" in response or "Wrong" in response:
            stdscr.move(3, 0)
            stdscr.clrtoeol()
            stdscr.addstr(response)
            stdscr.refresh()
        else:
            stdscr.move(2, 0)
            stdscr.clrtoeol()
            stdscr.addstr(response)
            stdscr.refresh()


        if "lose" in response:
            stdscr.move(0, 0)
            stdscr.clrtobot()
            stdscr.addstr(response)
            stdscr.move(1, 0)
            stdscr.addstr("Press any key to exit.")
            stdscr.refresh()
            stdscr.getch()
            break

        if "win" in response:
            stdscr.move(0, 0)
            stdscr.clrtobot()
            stdscr.addstr("Congratulations! You won!")
            stdscr.move(1, 0)
            stdscr.addstr("Press any key to exit.")
            stdscr.refresh()
            stdscr.getch()
            break

    client_socket.close()

if __name__ == "__main__":
    wrapper(main)

