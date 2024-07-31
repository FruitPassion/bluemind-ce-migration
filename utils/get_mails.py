from tqdm import tqdm
import time
from utils.coloration import colour_print
from utils.ssh_connexion import ssh_connect, close_connection, privilege_escalation
from dotenv import load_dotenv
import re
import os


load_dotenv("envs/.ssh.env")
load_dotenv("envs/.static.env")


def retrieve_mails(domaines):
    hostname = os.getenv('SOUR_HOSTNAME')
    port = int(os.getenv('SOUR_PORT'))
    username = os.getenv('SOUR_SSH_USER')
    password = os.getenv('SOUR_SSH_PASSWORD')
    raw_emails = []

    try:
        session, client = ssh_connect(hostname, port, username, password)

        if not privilege_escalation(session, password):
            close_connection(client, hostname)
            return None

        for line in tqdm(domaines, desc='Processing Domains'):
            command = f'bm-cli user get {line.strip()} --display email'
            time.sleep(1)
            session.send(f'{command}\n')

            time.sleep(2)
            output = session.recv(65535).decode('utf-8')
            raw_emails.append(output)
            colour_print(f"Mails for domains in {line.strip()} have been successfully retrieved", 'success')

        close_connection(client, hostname)
        return raw_emails

    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None


def raw_emails_process(raw_emails):
    try:
        colour_print("Processing raw emails", 'success')
        emails = []
        email_pattern = re.compile(r'{"email":"([^"]+)"}')
        for global_mails in tqdm(raw_emails, desc='Processing Raw Emails'):
            matches = email_pattern.findall(global_mails)
            for email in matches:
                emails.append(email)

        colour_print("Emails have been successfully extracted", 'success')
        colour_print("Total emails extracted: " + str(len(emails)), 'info')
        print()
        return emails
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None


def write_emails(emails):
    email_list = os.getenv('EMAILS')
    with open(email_list, 'w') as file:
        for email in emails:
            file.write(email)
            file.write('\n')


def main(domaines):
    raw_emails = retrieve_mails(domaines)
    if raw_emails is not None:
        emails = raw_emails_process(raw_emails)
        write_emails(emails)
