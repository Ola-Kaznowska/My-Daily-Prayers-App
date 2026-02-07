import sys
import time
from colorama import init, Fore, Style


init(autoreset=True)

# =====================
# CONFIGURATION
# =====================
PASSWORD = "islam123"  # change to your own

PRAYERS = [
    {"name": "Fajr", "time": "morning (before sunrise)", "done": False},
    {"name": "Dhuhr", "time": "midday", "done": False},
    {"name": "Asr", "time": "afternoon", "done": False},
    {"name": "Maghrib", "time": "evening (after sunset)", "done": False},
    {"name": "Isha", "time": "night", "done": False},
]



def input_password(prompt="Password: "):
    """Reads password with asterisk masking (*). Works on Windows / Linux / macOS."""
    print(prompt, end="", flush=True)
    password = ""

    try:
        
        import msvcrt
        while True:
            char = msvcrt.getch()
            if char in (b"\r", b"\n"):
                print()
                break
            elif char == b"\x08":  
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            else:
                password += char.decode("utf-8")
                print("*", end="", flush=True)
    except ImportError:
        
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char in ("\n", "\r"):
                    print()
                    break
                elif char == "\x7f":  # backspace
                    if len(password) > 0:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                else:
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password



def login():
    print(Fore.CYAN + "=== Daily Prayer Reminder ===")
    for attempt in range(3):
        entered = input_password(Fore.YELLOW + "Enter password: ")
        if entered == PASSWORD:
            print(Fore.GREEN + "Login successful!\n")
            return True
        else:
            print(Fore.RED + "Incorrect password!\n")
    print(Fore.RED + "Too many failed attempts. Exiting program.")
    return False



def show_prayers():
    print(Fore.CYAN + "\nYour daily prayers:\n")
    for i, p in enumerate(PRAYERS, start=1):
        status = Fore.GREEN + "✓ completed" if p["done"] else Fore.RED + "✗ not completed"
        print(
            Fore.YELLOW + f"{i}. {p['name']}" + Style.RESET_ALL
            + f" — {p['time']} | " + status
        )
    print()



def menu():
    while True:
        show_prayers()
        print(Fore.CYAN + "Menu:")
        print(Fore.WHITE + "1 - Mark a prayer as completed")
        print(Fore.WHITE + "2 - Reset prayer status")
        print(Fore.WHITE + "0 - Exit\n")

        choice = input(Fore.YELLOW + "Your choice: ")

        if choice == "1":
            try:
                num = int(input(Fore.YELLOW + "Enter prayer number (1-5): "))
                if 1 <= num <= 5:
                    PRAYERS[num - 1]["done"] = True
                    print(Fore.GREEN + "Prayer marked as completed.\n")
                else:
                    print(Fore.RED + "Invalid number.\n")
            except ValueError:
                print(Fore.RED + "That is not a number.\n")

        elif choice == "2":
            for p in PRAYERS:
                p["done"] = False
            print(Fore.GREEN + "Prayer status reset.\n")

        elif choice == "0":
            print(Fore.CYAN + "Peace be upon you. Assalamu Alaikum 🌙")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Unknown option.\n")




if __name__ == "__main__":
    if login():
        menu()