from os import path, makedirs, listdir, remove
from sys import stdin, stdout
from shutil import copy2, rmtree


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


# * BACKUP SECTION


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


# * UNINSTALL SECTION


def uninstall():
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()

    print_green("\nUNINSTALL")
    print("-" * 9)

    if path.exists(venv_path) is False and path.exists(desktop_file_path) is False:
        print_green("\nApplication not installed.\n")

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

        print_green("\nApplication uninstalled successfully.")


def main():
    uninstall()


if __name__ == "__main__":
    main()
