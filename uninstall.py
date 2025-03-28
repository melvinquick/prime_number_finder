import os
import sys
import shutil


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


# * BACKUP SECTION


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
        print_green("\nApplication not installed.\n")

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

        print_green("\nApplication uninstalled successfully.")


def main():
    uninstall()


if __name__ == "__main__":
    main()
