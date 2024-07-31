#!.venv/bin/python3
from tqdm import tqdm
from dotenv import load_dotenv
from utils.coloration import colour_print
import os
import csv
import secrets
import string

load_dotenv()


def generate_password(length=20):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_+"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def add_annex_entry(email, password_annex):
    password_annex[email] = generate_password()


def create_annex():
    email_list = os.getenv('EMAILS')
    with open(email_list, 'r') as file:
        lines = file.readlines()
    password_annex = {}
    colour_print("Generating Passwords...", 'warning')
    for line in tqdm(lines, desc='Generating Passwords', unit='emails'):
        add_annex_entry(line.strip(), password_annex)
    colour_print("Passwords have been successfully generated", 'success')
    colour_print(f'{len(password_annex)} passwords have been generated', 'success')
    print()
    return password_annex


def dict_to_csv(dictionary):
    colour_print("Writing to CSV...", 'warning')
    password_list = os.getenv('PASSWORDS')
    with open(password_list, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Password'])
        for key, value in dictionary.items():
            writer.writerow([key, value])
    colour_print("Passwords have been successfully written to the CSV file", 'success')
    print()


def main():
    password_annex = create_annex()
    dict_to_csv(password_annex)


if __name__ == '__main__':
    main()
