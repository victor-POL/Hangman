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


def draw_stick_man(stdscr, attempts):
    if attempts == 9:
        stdscr.addstr(4, 2, "|")

    if attempts == 8:
        stdscr.addstr(5, 2, "|")

    if attempts == 7:
        stdscr.addstr(6, 2, "O")

    if attempts == 6:
        stdscr.addstr(7, 1, "/")

    if attempts == 5:
        stdscr.addstr(7, 2, "|")

    if attempts == 4:
        stdscr.addstr(7, 3, "\\")

    if attempts == 3:
        stdscr.addstr(8, 2, "|")

    if attempts == 2:
        stdscr.addstr(9, 2, "/")

    if attempts == 1:
        stdscr.addstr(9, 3, "\\")

    stdscr.refresh()


def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)

    client_socket.connect((host, port))

    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Hangman! Guess a letter.")
    stdscr.addstr(1, 0, "Input letter: ")
    stdscr.refresh()

    attempts = 9
    while True:
        guess = chr(stdscr.getch()).lower()

        client_socket.send(guess.encode())

        response = client_socket.recv(1024).decode()

        if "Invalid" in response or "Wrong" in response:
            if "Wrong" in response:
                draw_stick_man(stdscr, attempts)
            stdscr.move(3, 0)
            stdscr.clrtoeol()
            stdscr.addstr(response)
            stdscr.refresh()
            attempts -= 1
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
