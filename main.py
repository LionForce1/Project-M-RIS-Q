## Imports
import os
import sys
import subprocess
import asyncio
import datetime
import threading
import time

from Utils.umanager import *
from Core.db_requests import init_db
from Core.menu import main_menu


## [ LIMPIAR TERMINAL ]
def clear_console():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        log_error("clear_console", e)

## [ BANNER ]
def print_banner():
    try:
        print("                                                                   ")
        print("\033[90m __  __      _     _           _____         _             ")
        print("\033[90m|  \/  | ___(_)___| |_ ___ _ _|_   _|__  ___| |__          ")
        print("\033[90m| |\/| |/ _ \ / __| __/ _ \ '__|| |/ _ \/ __| '_ \         ")
        print("\033[90m| |  | |  __/ \__ \ ||  __/ |   | |  __/ (__| | | |        ")
        print("\033[90m|_|  |_|\___|_|___/\__\___|_|   |_|\___|\___|_| |_|  Mk.0  ")
        print("                                                                   ")
        print("\033[90m==================[ By L Incorporated ]====================")
        print("                                                                   ")
    except Exception as e:
        log_error("print_banner", e)


## [ STARTUP ]
def startup():
    clear_console() ## Limpiar Terminal
    log("INFO", "Boot sequence started") ## Log de inicio de secuencia de Install/Update requirements
    ensure_requirements() ## Llamada a Funcion desde el umanager.py

    log("INFO", "Initializing database") ## Inicia la base de datos...
    init_db()

    print_banner() ## Print banner
    log("INFO", "System ready")

## [ MAIN ]
def main(): 
    startup()
    time.sleep(2)
    try:
        main_menu()

    except KeyboardInterrupt:
        log_warn("Shutdown requested by user")

    except Exception as e:
        log_error("main", e)

    finally:
        log("INFO", "System stopped")

## [ START ]
if __name__ == "__main__":
    main()