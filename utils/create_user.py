import tqdm
import time
from utils import parameters
from utils.coloration import colour_print
from utils.ssh_connexion import ssh_connect, close_connection, privilege_escalation
from dotenv import load_dotenv
import os


load_dotenv("envs/.ssh.env")
load_dotenv("envs/.static.env")


def create_user(emails, create_password):
    hostname = os.getenv('DEST_HOSTNAME')
    port = int(os.getenv('DEST_PORT'))
    ssh_user = os.getenv('DEST_SSH_USER')
    ssh_password = os.getenv('DEST_SSH_PASSWORD')
    try:
        session, client = ssh_connect(hostname, port, ssh_user, ssh_password)

        if not privilege_escalation(session, ssh_password):
            close_connection(client, hostname)
            return None

        email_to_password = {user['Email']: user['Password'] for user in parameters.get_parameter("PASSWORDS")}
        pbar = tqdm.tqdm(total=len(emails), desc='Creating Users', unit='user')

        for email in emails:
            command = f'bm-cli user quickcreate {email}'
            session.send(f'{command}\n')
            time.sleep(10)
            pbar.write(f"User {email} has been successfully created")

            if create_password and email in email_to_password:
                password_user = email_to_password[email]
                command = f'bm-cli user update {email} --password="{password_user}" --set-password-must-change'
                session.send(f'{command}\n')
                time.sleep(10)
                pbar.write(f"Password for {email} has been successfully updated")

            pbar.update(1)
            time.sleep(1)

        pbar.close()
        colour_print("Users have been successfully created", 'success')
        close_connection(client, hostname)

    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None


def main(emails, password):
    create_user(emails, password)
