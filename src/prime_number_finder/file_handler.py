import os
import yaml


class PrimeFileHandler:
    def __init__(self):
        self.prime_numbers_file = self.get_file_path("resources/data/prime_numbers.txt")
        self.current_number_file = self.get_file_path(
            "resources/data/current_number.txt"
        )
        self.prime_list = []

    def get_file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def load_prime_numbers(self):
        with open(self.prime_numbers_file, "r") as f:
            for prime in f:
                self.prime_list.append(int(prime))
            return self.prime_list

    def save_found_prime(self, prime):
        with open(self.prime_numbers_file, "a") as f:
            f.write(f"{str(prime)}\n")
            return

    def load_current_number(self):
        with open(self.current_number_file, "r") as f:
            return int(f.read())

    def save_current_number(self, number):
        with open(self.current_number_file, "w") as f:
            f.write(str(number))
            return


class YamlFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def load_yaml_file(self):
        with open(self.get_file_path(), "r") as f:
            return yaml.safe_load(f)

    def save_yaml_file(self, configs):
        with open(self.get_file_path(), "w") as f:
            return yaml.safe_dump(configs, f, default_flow_style=False)

    def get_file_path(self):
        return os.path.join(os.path.dirname(__file__), self.filename)
