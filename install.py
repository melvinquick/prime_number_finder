import os
import re
import shutil
import subprocess
import sys
from textwrap import dedent
from urllib.request import urlopen
from urllib.error import URLError


def print_green(skk):
    print(f"\033[92m {skk}\033[00m")


def print_red(skk):
    print(f"\033[91m {skk}\033[00m")


def get_project_metadata():
    """Read name and description from pyproject.toml.

    Search order:
      1. Same directory as this script (when run as a real file)
      2. Parent of the script
      3. Current working directory
      4. Parent of the current working directory
      5. Remote fallback (GitHub raw) when run via curl | python
    """
    candidates = []

    # Local file locations (only when the script exists on disk)
    if "__file__" in globals() and os.path.isfile(__file__):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(script_dir, "pyproject.toml"))
        candidates.append(os.path.join(script_dir, "..", "pyproject.toml"))

    # Current working directory (covers both local runs and some remote cases)
    cwd = os.getcwd()
    candidates.append(os.path.join(cwd, "pyproject.toml"))
    candidates.append(os.path.join(cwd, "..", "pyproject.toml"))

    content = None
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            break

    # Remote fallback for `curl ... | python3 -`
    if content is None:
        remote_url = (
            "https://raw.githubusercontent.com/melvinquick/phaino/main/pyproject.toml"
        )
        try:
            with urlopen(remote_url, timeout=10) as response:
                content = response.read().decode("utf-8")
        except (URLError, TimeoutError, OSError):
            content = None

    if content is None:
        print_red("Error: Could not find pyproject.toml locally or remotely")
        sys.exit(1)

    name_match = re.search(
        r'^\s*name\s*=\s*["\']([^"\']+)["\']',
        content,
        re.MULTILINE,
    )
    desc_match = re.search(
        r'^\s*description\s*=\s*["\']([^"\']+)["\']',
        content,
        re.MULTILINE,
    )

    if not name_match:
        print_red("Error: Could not parse name from pyproject.toml")
        sys.exit(1)

    name = name_match.group(1)
    description = desc_match.group(1) if desc_match else ""
    return name, description


# Read metadata and derive all name variants
PACKAGE_NAME, DESCRIPTION = get_project_metadata()
EXECUTABLE_NAME = PACKAGE_NAME.replace("_", "-")
DISPLAY_NAME = " ".join(w.capitalize() for w in PACKAGE_NAME.split("_"))

# Path fragments built from PACKAGE_NAME
VENV_NAME = f"{PACKAGE_NAME}_venv"
DESKTOP_FILENAME = f"{PACKAGE_NAME}.desktop"
ICON_RELATIVE_PATH = f"{PACKAGE_NAME}/resources/images/{PACKAGE_NAME}-128.png"
DATABASE_RELATIVE_PATH = f"{PACKAGE_NAME}/resources/data/prime_data.db"
BACKUP_DIR = os.path.expanduser("~/found_primes_backup")
BACKUP_DB_PATH = os.path.join(BACKUP_DIR, "prime_data.db")


def get_venv_path():
    home_dir = os.path.expanduser("~")
    venv_dir = os.path.join(home_dir, ".venvs")
    if not os.path.exists(venv_dir):
        os.makedirs(venv_dir)
    return os.path.join(venv_dir, VENV_NAME)


def get_site_package_path(venv_path):
    site_packages = os.path.join(venv_path, "lib")
    for folder in os.listdir(site_packages):
        if folder.startswith("python"):
            return os.path.join(site_packages, folder, "site-packages")
    return None


def get_desktop_file_path():
    return os.path.expanduser(f"~/.local/share/applications/{DESKTOP_FILENAME}")


# ---------------------------------------------------------------------------
# Backup / Restore
# ---------------------------------------------------------------------------


def prompt_yes_no(question):
    if not sys.stdin.isatty():
        return "y"
    return input(question).lower().strip()


def backup(site_package_path):
    if site_package_path is None:
        return
    choice = prompt_yes_no("Do you want to back up your found prime files? (y/n): ")
    if choice == "y":
        backup_found_prime_files(site_package_path)
    elif choice == "n":
        print("Backup declined.")
    else:
        print("Invalid input. Skipping backup.")


def backup_found_prime_files(site_packages):
    database_app_path = os.path.join(site_packages, DATABASE_RELATIVE_PATH)

    if not os.path.exists(database_app_path):
        print("App database not found. Skipping backup.")
        return

    print(f"Backing up database to {BACKUP_DB_PATH}...", end=" ")
    sys.stdout.flush()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy2(database_app_path, BACKUP_DB_PATH)
    print_green("[OK]")


def restore(site_package_path):
    if site_package_path is None or not os.path.exists(BACKUP_DB_PATH):
        return
    choice = prompt_yes_no("Do you want to restore your found prime files? (y/n): ")
    if choice == "y":
        restore_found_prime_files(site_package_path)
    elif choice == "n":
        print("Restore declined.")
    else:
        print("Invalid input. Skipping restore.")


def restore_found_prime_files(site_packages):
    database_app_path = os.path.join(site_packages, DATABASE_RELATIVE_PATH)

    print("Restoring database to app path...", end=" ")
    sys.stdout.flush()

    os.makedirs(os.path.dirname(database_app_path), exist_ok=True)
    shutil.copy2(BACKUP_DB_PATH, database_app_path)
    print_green("[OK]")


# ---------------------------------------------------------------------------
# Core install / uninstall
# ---------------------------------------------------------------------------


def create_venv(venv_path):
    print("Creating the virtual environment...", end=" ")
    sys.stdout.flush()
    subprocess.run(
        [sys.executable, "-m", "venv", venv_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")

    print("Ensuring pip is up to date...", end=" ")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--upgrade", "pip"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")


def install_app(venv_path):
    print(f"Installing {DISPLAY_NAME} into the virtual environment...", end=" ")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--no-cache-dir", PACKAGE_NAME],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")


def get_installed_version(venv_path):
    """Read version from installed package metadata inside the venv."""
    python_path = os.path.join(venv_path, "bin", "python3")
    result = subprocess.run(
        [
            python_path,
            "-c",
            f"from importlib.metadata import version; print(version('{PACKAGE_NAME}'))",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_icon(site_packages):
    return os.path.join(site_packages, ICON_RELATIVE_PATH)


def get_python_path(venv_path):
    return os.path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return os.path.join(venv_path, "bin", EXECUTABLE_NAME)


def create_desktop_file(icon, version, python, app):
    print("Creating the .desktop entry...", end=" ")
    sys.stdout.flush()

    desktop_content = dedent(f"""\
        [Desktop Entry]
        Version={version}
        Type=Application
        Name={DISPLAY_NAME}
        Comment={DESCRIPTION}
        Exec={python} {app}
        Icon={icon}
        Terminal=false
        Categories=Utility;
    """)

    desktop_path = get_desktop_file_path()
    os.makedirs(os.path.dirname(desktop_path), exist_ok=True)

    with open(desktop_path, "w") as f:
        f.write(desktop_content)
    print_green("[OK]")


def do_uninstall(offer_backup=True):
    """Removes venv and desktop file. Optionally offers backup first.
    Returns True if anything was removed."""
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()
    removed = False

    if os.path.exists(venv_path):
        if offer_backup:
            site_package_path = get_site_package_path(venv_path)
            backup(site_package_path)
        print("Removing the virtual environment...", end=" ")
        sys.stdout.flush()
        shutil.rmtree(venv_path)
        print_green("[OK]")
        removed = True
    else:
        print("No virtual environment found.")

    if os.path.exists(desktop_file_path):
        print("Removing the .desktop entry...", end=" ")
        sys.stdout.flush()
        os.remove(desktop_file_path)
        print_green("[OK]")
        removed = True
    else:
        print("No .desktop entry found.")

    return removed


def do_install(offer_restore=True):
    """Fresh install: creates venv, installs app, creates desktop entry.
    Optionally offers restore if a backup exists."""
    venv_path = get_venv_path()
    create_venv(venv_path)
    install_app(venv_path)

    version = get_installed_version(venv_path)
    site_package_path = get_site_package_path(venv_path)

    icon = get_icon(site_package_path)
    python = get_python_path(venv_path)
    app = get_app_path(venv_path)
    create_desktop_file(icon, version, python, app)

    if offer_restore and os.path.exists(BACKUP_DB_PATH):
        restore(site_package_path)

    print()
    print_green(f"{DISPLAY_NAME} v{version} has been successfully installed.")


def handle_update():
    """Update = full uninstall (with backup) followed by fresh install (with restore)."""
    print(f"\nUpdating {DISPLAY_NAME}...\n")
    existed = do_uninstall(offer_backup=True)
    if not existed:
        print("No existing installation found. Performing fresh install.\n")
    else:
        print()
    do_install(offer_restore=True)


def show_menu():
    try:
        with open("/dev/tty", "r") as tty:
            while True:
                print(f"\n=== {DISPLAY_NAME} Installer ===")
                print("1) Install")
                print("2) Update")
                print("3) Uninstall")
                print("0) Exit")

                sys.stdout.write("\nSelect an option [0-3]: ")
                sys.stdout.flush()
                choice = tty.readline().strip()

                if choice == "1":
                    venv_path = get_venv_path()
                    if os.path.exists(venv_path):
                        print_red(
                            "\nExisting installation detected. Please use 'Update' instead."
                        )
                        continue
                    print()
                    do_install(offer_restore=True)
                    break

                elif choice == "2":
                    handle_update()
                    break

                elif choice == "3":
                    print()
                    if do_uninstall(offer_backup=True):
                        print()
                        print_green(f"{DISPLAY_NAME} has been uninstalled.")
                    else:
                        print(f"\n{DISPLAY_NAME} does not appear to be installed.")
                    break

                elif choice == "0":
                    print("\nGoodbye.")
                    break

                else:
                    print_red("\nInvalid selection. Please try again.")
    except OSError:
        print_red("Error: No interactive terminal available.")
        print_red("Please run this script from a terminal session.")
        sys.exit(1)


def main():
    show_menu()


if __name__ == "__main__":
    main()
