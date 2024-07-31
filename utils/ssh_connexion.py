import warnings

warnings.filterwarnings("ignore")

import paramiko
import time
from utils.coloration import colour_print


def ssh_connect(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        colour_print("Connecting to the server...", 'warning')
        client.connect(hostname=hostname, port=port, username=username, password=password)
        colour_print("Connected to the server " + hostname, 'success')
        time.sleep(1)
        session = client.invoke_shell()
        return session, client
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None, None


def check_privilege(session):
    try:
        time.sleep(1)
        session.send('sudo -l\n')

        time.sleep(1)
        resp = session.recv(65535).decode()
        if 'not allowed to run sudo' in resp:
            return False
        return True
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None


def privilege_escalation(session, password):
    """
    if not check_privilege(session):
        colour_print("User does not have sudo privileges", 'error')
        return False
    """
    try:
        time.sleep(1)
        session.send('sudo su -\n')

        time.sleep(1)
        resp = session.recv(65535).decode()

        time.sleep(1)
        if not resp.endswith('# '):
            session.send(f'{password}\n')
            time.sleep(3)
            resp = session.recv(65535).decode()
            colour_print("Privilege escalation successful", 'success')
            return True
        else:
            colour_print("Failed to escalate privileges", 'error')
            return False
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None, None


def close_connection(client, hostname):
    try:
        client.close()
        colour_print("Connection closed for " + hostname, 'success')
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        return None
