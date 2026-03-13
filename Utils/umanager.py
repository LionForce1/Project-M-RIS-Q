import datetime
import os
import sys
import subprocess
import importlib

# [ CONFIGURACION ]

APP_NAME = "MeisterTech"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(ROOT, "Logs")
LOG_FILE = os.path.join(LOG_DIR, "system.log")

os.makedirs(LOG_DIR, exist_ok=True)

## [ Colores Arte ASCII]
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_UNDER = "\033[4m"

CLR_GREY = "\033[90m"
CLR_RED = "\033[91m"
CLR_GREEN = "\033[92m"
CLR_YELLOW = "\033[93m"
CLR_BLUE = "\033[94m"

## [ Funcion De Update o Install Requirements ]
def ensure_requirements():

    def managed_env():
        candidates = [
            os.path.join(sys.prefix, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'EXTERNALLY-MANAGED'),
            os.path.join(sys.prefix, 'EXTERNALLY-MANAGED'),
            os.path.join(sys.base_prefix, 'EXTERNALLY-MANAGED'),
        ]
        return any(os.path.exists(p) for p in candidates)

    def missing(pkgs):
        miss = []
        for p in pkgs:
            name = p.split("==")[0].split(">=")[0].split("~=")[0].strip()
            try:
                importlib.import_module(name.replace('-', '_'))
            except Exception:
                miss.append(p)
        return miss

    req = os.path.join(ROOT, "requirements.txt")

    if not os.path.exists(req):
        log("WARN", "No requirements.txt found")
        return

    # Detectar virtualenv
    in_venv = hasattr(sys, "real_prefix") or (sys.prefix != sys.base_prefix)

    venv_dir = os.path.join(ROOT, ".venv")

    # Si no estamos en venv
    if not in_venv:

        if not os.path.exists(venv_dir):

            log("INFO", "Creating virtual environment (.venv)")

            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

        py = (
            os.path.join(venv_dir, "Scripts", "python.exe")
            if os.name == "nt"
            else os.path.join(venv_dir, "bin", "python")
        )

        log("INFO", "Installing dependencies inside .venv")

        subprocess.check_call([py, "-m", "pip", "install", "-U", "pip"])
        subprocess.check_call([py, "-m", "pip", "install", "-r", req])

        log("INFO", "Dependencies installed successfully")

        os.execv(py, [py] + sys.argv)

    # Ya estamos dentro del venv
    with open(req, "r", encoding="utf-8") as f:
        deps = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    need = missing(deps)

    if not need:
        log("INFO", "All dependencies satisfied")
        return

    log("INFO", "Installing missing dependencies")

    cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + need

    completed = subprocess.run(cmd, capture_output=True, text=True)

    if completed.returncode == 0:
        log("INFO", "Dependencies installed")
        return

    if managed_env():
        log_warn("Managed environment detected, retrying with break-system-packages")
        cmd.append("--break-system-packages")
        subprocess.check_call(cmd)
        return

    raise RuntimeError(completed.stderr)

## [ Sistema De Logs ]
def _classify(level: str) -> str:
    t = (level or "").upper()

    if t == "ERROR":
        return "error"

    if t in ("WARN", "WARNING"):
        return "warn"

    return "info"


def log(type_: str, message: str):

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prefix = f"{CLR_GREY}{ANSI_UNDER}{APP_NAME}{ANSI_RESET}  :: "

    category = _classify(type_)

    t_upper = (type_ or "INFO").upper()

    if category == "error":
        sym_char = "-"
        sym_color = CLR_RED
        tag_plain = "ERROR"

    elif category == "warn":
        sym_char = "!"
        sym_color = CLR_YELLOW
        tag_plain = "WARN"

    else:
        sym_char = "+"
        sym_color = CLR_GREEN
        tag_plain = t_upper

    symbol = f"{CLR_GREY}[{ANSI_RESET}{sym_color}{sym_char}{ANSI_RESET}{CLR_GREY}]{ANSI_RESET}"

    print(f"{prefix}{symbol} {message}")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{current_time} - {APP_NAME} :: [{sym_char}] {tag_plain.ljust(8)} {message}\n")


def log_error(origin: str, error: Exception):
    log("ERROR", f"[{origin}] {error}")


def log_warn(message: str):
    log("WARN", message)


def write_file(type_: str, message: str):

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tag_plain = (type_ or "INFO").upper().ljust(8)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{current_time} {tag_plain} {message}\n")