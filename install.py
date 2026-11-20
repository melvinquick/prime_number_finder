import os
import shutil
import subprocess
import sys
from textwrap import dedent


# ---------------------------------------------------------------------------
# Project identifier: comes from the command line, NOT hardcoded.
# Usage:  curl ... | python3 - <package_name>
# Example: curl ... | python3 - prime_number_finder
# ---------------------------------------------------------------------------
def resolve_package_name():
    """Return the pip/import name from argv, or prompt for it."""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()

    # Fallback: prompt interactively (only if a TTY is available)
    try:
        with open("/dev/tty", "r") as tty:
            sys.stdout.write("Enter the Python package name to install: ")
            sys.stdout.flush()
            name = tty.readline().strip()
            if not name:
                raise ValueError("Empty package name")
            return name
    except (OSError, ValueError) as exc:
        print(f"Error: no package name provided ({exc}).", file=sys.stderr)
        print("Usage: curl ... | python3 - <package_name>", file=sys.stderr)
        sys.exit(2)


PACKAGE_NAME = resolve_package_name()


# ---------------------------------------------------------------------------
# All name variants are derived from PACKAGE_NAME.
# ---------------------------------------------------------------------------
def derive_names(pkg: str) -> dict:
    """Compute every name/path fragment from a single package name."""
    return {
        # The pip/import name, e.g. "prime_number_finder"
        "package": pkg,
        # Console-script / executable name, e.g. "prime-number-finder"
        "executable": pkg.replace("_", "-"),
        # Human-readable display name, e.g. "Prime Number Finder"
        "display": " ".join(w.capitalize() for w in pkg.split("_")),
        # Virtualenv directory name, e.g. "prime_number_finder_venv"
        "venv": f"{pkg}_venv",
        # .desktop file name, e.g. "prime_number_finder.desktop"
        "desktop_filename": f"{pkg}.desktop",
        # Icon path inside site-packages
        "icon_relative": f"{pkg}/resources/images/{pkg}-128.png",
        # Database path inside site-packages
        "database_relative": f"{pkg}/resources/data/prime_data.db",
        # Backup directory (project-scoped so multiple installs don't collide)
        "backup_dir": os.path.expanduser(f"~/.local/share/{pkg}/backup"),
        # Backup database file name (fixed, lives inside backup_dir)
        "backup_db_filename": "prime_data.db",
    }


NAMES = derive_names(PACKAGE_NAME)

# Short-hand aliases used throughout the script
EXECUTABLE_NAME = NAMES["executable"]
DISPLAY_NAME = NAMES["display"]
VENV_NAME = NAMES["venv"]
DESKTOP_FILENAME = NAMES["desktop_filename"]
ICON_RELATIVE_PATH = NAMES["icon_relative"]
DATABASE_RELATIVE_PATH = NAMES["database_relative"]
BACKUP_DIR = NAMES["backup_dir"]
BACKUP_DB_PATH = os.path.join(BACKUP_DIR, NAMES["backup_db_filename"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def print_green(skk):
    print(f"\033[92m {skk}\033[00m")


def print_red(skk):
    print(f"\033[91m {skk}\033[00m")


def get_venv_path():
    venv_dir = os.path.expanduser("~/.venvs")
    os.makedirs(venv_dir, exist_ok=True)
    return os.path.join(venv_dir, VENV_NAME)


def get_site_package_path(venv_path):
    site_packages = os.path.join(venv_path, "lib")
    if not os.path.isdir(site_packages):
        return None
    for folder in os.listdir(site_packages):
        if folder.startswith("python"):
            return os.path.join(site_packages, folder, "site-packages")
    return None


def get_desktop_file_path():
    return os.path.expanduser(f"~/.local/share/applications/{DESKTOP_FILENAME}")


# ---------------------------------------------------------------------------
# Backup / Restore
# ---------------------------------------------------------------------------
def backup_found_prime_files(site_packages):
    if site_packages is None:
        return
    database_app_path = os.path.join(site_packages, DATABASE_RELATIVE_PATH)
    if not os.path.exists(database_app_path):
        print("App database not found. Skipping backup.")
        return

    print(f"Backing up database to {BACKUP_DB_PATH}...", end=" ")
    sys.stdout.flush()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy2(database_app_path, BACKUP_DB_PATH)
    print_green("[OK]")


def restore_found_prime_files(site_packages):
    if site_packages is None or not os.path.exists(BACKUP_DB_PATH):
        return
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


def get_installed_metadata(venv_path):
    """Read version and description from the installed package inside the venv."""
    python_path = os.path.join(venv_path, "bin", "python3")
    result = subprocess.run(
        [
            python_path,
            "-c",
            (
                "from importlib.metadata import metadata; "
                f"m = metadata('{PACKAGE_NAME}'); "
                "print(m['Version']); "
                "print(m.get('Summary', ''))"
            ),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    version = lines[0] if lines else "unknown"
    description = lines[1] if len(lines) > 1 else ""
    return version, description


def get_icon(site_packages):
    return os.path.join(site_packages, ICON_RELATIVE_PATH)


def get_python_path(venv_path):
    return os.path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return os.path.join(venv_path, "bin", EXECUTABLE_NAME)


def create_desktop_file(icon, version, description, python, app):
    print("Creating the .desktop entry...", end=" ")
    sys.stdout.flush()

    desktop_content = dedent(f"""\
        [Desktop Entry]
        Version={version}
        Type=Application
        Name={DISPLAY_NAME}
        Comment={description}
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


def do_uninstall():
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()
    removed = False

    if os.path.exists(venv_path):
        site_package_path = get_site_package_path(venv_path)
        backup_found_prime_files(site_package_path)
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


def do_install():
    venv_path = get_venv_path()
    create_venv(venv_path)
    install_app(venv_path)

    version, description = get_installed_metadata(venv_path)
    site_package_path = get_site_package_path(venv_path)

    icon = get_icon(site_package_path)
    python = get_python_path(venv_path)
    app = get_app_path(venv_path)
    create_desktop_file(icon, version, description, python, app)

    restore_found_prime_files(site_package_path)

    print()
    print_green(f"{DISPLAY_NAME} v{version} has been successfully installed.")


def handle_update():
    print(f"\nUpdating {DISPLAY_NAME}...\n")
    existed = do_uninstall()
    if not existed:
        print("No existing installation found. Performing fresh install.\n")
    else:
        print()
    do_install()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
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
                            "\nExisting installation detected. "
                            "Please use 'Update' instead."
                        )
                        continue
                    print()
                    do_install()
                    break

                elif choice == "2":
                    handle_update()
                    break

                elif choice == "3":
                    print()
                    if do_uninstall():
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
