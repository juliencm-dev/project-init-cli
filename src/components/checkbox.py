import sys
import tty
import termios
import os

os.environ["PYTHONUNBUFFERED"] = "1"


options = ["Python", "Golang"]
selected = set()
current = 0

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def print_menu():
    sys.stderr.write("\033[?25l")
    for idx, option in enumerate(options):
        checkbox = "x" if idx in selected else " "
        cursor = ">" if idx == current else " "
        print(f"{cursor}[{checkbox}] {option}", file=sys.stderr, flush=True)

try:
    while True:
        print_menu()
        key = get_key()
        sys.stderr.write("\033[F"*(len(options)))

        if key == "k":
            current = (current - 1) % len(options)
        elif key == "j":
            current = (current + 1) % len(options)
        elif key == " ":
            if current in selected:
                selected.remove(current)
            else:
                selected.clear()
                selected.add(current)
        elif key == "\r":
            selected_options = [options[i] for i in selected]
            print(" ".join(selected_options).lower(), flush=True) 
            break
finally:
    sys.stderr.write("\033[?25h") 
