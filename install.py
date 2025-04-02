from os import path, listdir, makedirs, remove
from sys import stdin, stdout
from subprocess import run, DEVNULL
from shutil import copy2, rmtree
from textwrap import dedent


def print_green(skk):
    print("\033[92m {}\033[00m".format(skk))


def get_venv_path():
    home_dir = path.expanduser("~")
    venv_dir = path.join(home_dir, ".venvs")
    if not path.exists(venv_dir):
        makedirs(venv_dir)
    return path.join(venv_dir, "prime_number_finder_venv")


def get_site_package_path(venv_path):
    site_packages = path.join(venv_path, "lib")
    for folder in listdir(site_packages):
        if folder.startswith("python"):
            return path.join(site_packages, folder, "site-packages")


def get_desktop_file_path():
    return path.expanduser("~/.local/share/applications/prime_number_finder.desktop")


# * BACKUP/RESTORE SECTION


def backup(site_package_path):
    if stdin.isatty() is False:
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
    backup_dir = path.expanduser("~/found_primes_backup/")
    database_app_path = path.join(
        site_packages, "prime_number_finder/resources/data/prime_data.db"
    )
    database_backup_path = path.join(backup_dir, "prime_data.db")

    if path.exists(database_app_path) is False:
        print(" App database not found. Skipping backup.")

    else:
        print(
            "Backing up database to $HOME/found_primes_backup/prime_data.db...", end=""
        )
        stdout.flush()

        if path.exists(backup_dir) is False:
            makedirs(backup_dir)

        copy2(database_app_path, database_backup_path)
        print_green("󰄬")


def restore(site_package_path):
    if stdin.isatty() is False:
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
    backup_dir = path.expanduser("~/found_primes_backup/")
    database_app_path = path.join(
        site_packages, "prime_number_finder/resources/data/prime_data.db"
    )
    database_backup_path = path.join(backup_dir, "prime_data.db")

    if path.exists(database_backup_path) is False:
        print("Backup database not found. Skipping restore.")

    else:
        print("Restoring database to app path...", end="")
        stdout.flush()

        copy2(database_backup_path, database_app_path)
        print_green("󰄬")


# * UNINSTALL SECTION


def uninstall():
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()

    print_green("\nUNINSTALL")
    print("-" * 9)

    if path.exists(venv_path) is False and path.exists(desktop_file_path) is False:
        print_green("\nApplication not installed... Moving on to installation.\n")

    else:
        if path.exists(venv_path):
            site_package_path = get_site_package_path(venv_path)
            backup(site_package_path)
            print("Removing the virtual environment...", end="")
            stdout.flush()
            rmtree(venv_path)
            print_green("󰄬")

        else:
            print("No virtual environment found...", end="")
            stdout.flush()
            print_green("󰄬")

        if path.exists(desktop_file_path):
            print("Removing the .desktop entry...", end="")
            stdout.flush()
            remove(desktop_file_path)
            print_green("󰄬")

        else:
            print("No .desktop entry found...", end="")
            stdout.flush()
            print_green("󰄬")

        print_green(
            "\nApplication uninstalled successfully... Moving on to installation."
        )


# * INSTALL SECTION


def create_venv(venv_path):
    print("Creating the virtual environment...", end="")
    stdout.flush()
    run(
        ["python3", "-m", "venv", venv_path],
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    print_green("󰄬")

    print("Ensuring pip is up to date...", end="")
    stdout.flush()
    pip_path = path.join(venv_path, "bin", "pip")
    run(
        [pip_path, "install", "--upgrade", "pip"],
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    print_green("󰄬")


def install_app(venv_path):
    print("Installing Prime Number Finder into the virtual environment...", end="")
    stdout.flush()
    pip_path = path.join(venv_path, "bin", "pip")
    run(
        [pip_path, "install", "prime_number_finder"],
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    print_green("󰄬")


def get_icon(site_packages):
    icon_relative_path = (
        "prime_number_finder/resources/images/prime_number_finder-128.png"
    )
    full_icon_path = path.join(site_packages, icon_relative_path)
    return full_icon_path


def get_python_path(venv_path):
    return path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return path.join(venv_path, "bin", "prime-number-finder")


def create_desktop_file(icon, version, python, app):
    print("Creating the .desktop entry...", end="")
    stdout.flush()
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
        path.expanduser("~/.local/share/applications/prime_number_finder.desktop"),
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
    version = "1.8.0"
    icon = get_icon(site_package_path)
    python = get_python_path(venv_path)
    app = get_app_path(venv_path)
    create_desktop_file(icon, version, python, app)

    backup_dir = path.expanduser("~/found_primes_backup/")

    if path.exists(backup_dir):
        restore(site_package_path)

    print_green("\nApplication has been installed successfully.")


def main():
    uninstall()
    install()


if __name__ == "__main__":
    main()
