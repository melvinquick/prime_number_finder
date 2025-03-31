import os
import sys
import subprocess
import shutil
from textwrap import dedent


def print_green(skk):
    print("\033[92m {}\033[00m".format(skk))


def get_venv_path():
    home_dir = os.path.expanduser("~")
    venv_dir = os.path.join(home_dir, ".venvs")
    if not os.path.exists(venv_dir):
        os.makedirs(venv_dir)
    return os.path.join(venv_dir, "prime_number_finder_venv")


def get_site_package_path(venv_path):
    site_packages = os.path.join(venv_path, "lib")
    for folder in os.listdir(site_packages):
        if folder.startswith("python"):
            return os.path.join(site_packages, folder, "site-packages")


def get_desktop_file_path():
    return os.path.expanduser("~/.local/share/applications/prime_number_finder.desktop")


# * BACKUP/RESTORE SECTION


def backup(site_package_path):
    if sys.stdin.isatty() is False:
        backup = "y"
    else:
        backup = input("Do you want to back up your found prime files? (y/n): ").lower()

    if backup == "y":
        backup_found_prime_files(site_package_path)
    elif backup == "n":
        print("Backups declined. Moving on to uninstall.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")


def backup_found_prime_files(site_packages):
    backup_dir = os.path.expanduser("~/found_primes_backup/")
    current_number_app_path = os.path.join(
        site_packages, "prime_number_finder/current_number.txt"
    )
    prime_list_app_path = os.path.join(
        site_packages, "prime_number_finder/prime_numbers.txt"
    )
    current_number_backup_path = os.path.join(backup_dir, "current_number.txt")
    prime_list_backup_path = os.path.join(backup_dir, "prime_numbers.txt")

    if (
        os.path.exists(current_number_app_path) is False
        or os.path.exists(prime_list_app_path) is False
    ):
        print("Backup files not found. Skipping backup.")

    else:
        print("Backing up files to $HOME/found_primes_backup...", end="")
        sys.stdout.flush()

        if os.path.exists(backup_dir) is False:
            os.makedirs(backup_dir)

        shutil.copy2(current_number_app_path, current_number_backup_path)
        shutil.copy2(prime_list_app_path, prime_list_backup_path)
        print_green("󰄬")


def restore(site_package_path):
    if sys.stdin.isatty() is False:
        restore = "y"
    else:
        restore = input(
            "Do you want to back up your found prime files? (y/n): "
        ).lower()

    if restore == "y":
        restore_found_prime_files(site_package_path)
    elif restore == "n":
        print("Restore declined. Finishing install.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")


def restore_found_prime_files(site_packages):
    backup_dir = os.path.expanduser("~/found_primes_backup/")
    current_number_app_path = os.path.join(
        site_packages, "prime_number_finder/current_number.txt"
    )
    prime_list_app_path = os.path.join(
        site_packages, "prime_number_finder/prime_numbers.txt"
    )
    current_number_backup_path = os.path.join(backup_dir, "current_number.txt")
    prime_list_backup_path = os.path.join(backup_dir, "prime_numbers.txt")

    if (
        os.path.exists(current_number_backup_path) is False
        or os.path.exists(prime_list_backup_path) is False
    ):
        print("Restore files not found. Skipping restore.")

    else:
        print("Restoring files to app path...", end="")
        sys.stdout.flush()

        shutil.copy2(current_number_backup_path, current_number_app_path)
        shutil.copy2(prime_list_backup_path, prime_list_app_path)
        print_green("󰄬")


# * UNINSTALL SECTION


def uninstall():
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()

    print_green("\nUNINSTALL")
    print("-" * 9)

    if (
        os.path.exists(venv_path) is False
        and os.path.exists(desktop_file_path) is False
    ):
        print_green("\nApplication not installed... Moving on to installation.\n")

    else:
        if os.path.exists(venv_path):
            site_package_path = get_site_package_path(venv_path)
            backup(site_package_path)
            print("Removing the virtual environment...", end="")
            sys.stdout.flush()
            shutil.rmtree(venv_path)
            print_green("󰄬")

        else:
            print("No virtual environment found...", end="")
            sys.stdout.flush()
            print_green("󰄬")

        if os.path.exists(desktop_file_path):
            print("Removing the .desktop entry...", end="")
            sys.stdout.flush()
            os.remove(desktop_file_path)
            print_green("󰄬")

        else:
            print("No .desktop entry found...", end="")
            sys.stdout.flush()
            print_green("󰄬")

        print_green(
            "\nApplication uninstalled successfully... Moving on to installation."
        )


# * INSTALL SECTION


def create_venv(venv_path):
    print("Creating the virtual environment...", end="")
    sys.stdout.flush()
    subprocess.run(
        ["python3", "-m", "venv", venv_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")

    print("Ensuring pip is up to date...", end="")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--upgrade", "pip"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")


def install_app(venv_path):
    print("Installing Prime Number Finder into the virtual environment...", end="")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "prime_number_finder"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")


def get_icon(site_packages):
    icon_relative_path = (
        "prime_number_finder/resources/images/prime_number_finder-128.png"
    )
    full_icon_path = os.path.join(site_packages, icon_relative_path)
    return full_icon_path


def get_python_path(venv_path):
    return os.path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return os.path.join(venv_path, "bin", "prime-number-finder")


def create_desktop_file(icon, version, python, app):
    print("Creating the .desktop entry...", end="")
    sys.stdout.flush()
    desktop_content = dedent(f"""
    [Desktop Entry]
    Version={version}
    Type=Application
    Name=Prime Number Finder
    Comment=Python program for finding/checking Prime Numbers.
    Exec={python} {app}
    Icon={icon}
    Terminal=false
    Categories=Utility;
    """)
    desktop_content = desktop_content.lstrip()
    with open(
        os.path.expanduser("~/.local/share/applications/prime_number_finder.desktop"),
        "w",
    ) as f:
        f.write(desktop_content)
    print_green("󰄬")


def install():
    print_green("\nINSTALL")
    print("-" * 7)

    venv_path = get_venv_path()
    create_venv(venv_path)
    install_app(venv_path)
    site_package_path = get_site_package_path(venv_path)
    version = "1.5.0"
    icon = get_icon(site_package_path)
    python = get_python_path(venv_path)
    app = get_app_path(venv_path)
    create_desktop_file(icon, version, python, app)

    backup_dir = os.path.expanduser("~/found_primes_backup/")

    if os.path.exists(backup_dir):
        restore(site_package_path)

    print_green("\nApplication has been installed successfully.")


def main():
    uninstall()
    install()


if __name__ == "__main__":
    main()
