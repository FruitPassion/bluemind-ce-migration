import smtplib
from email.mime.text import MIMEText
import tqdm
from utils import parameters
from utils.coloration import colour_print
from dotenv import load_dotenv
import os


load_dotenv("envs/.mails.env")
load_dotenv("envs/.static.env")
email_user = os.getenv('EMAIL_USER')
email_cc = os.getenv('EMAIL_CC')
email_host = os.getenv('EMAIL_HOST')
email_password = os.getenv('EMAIL_PASSWORD')
email_port = int(os.getenv('EMAIL_PORT'))
message_file = os.getenv('EMAIL_MESSAGE')


def send_mail(destinataire, sujet, message):
    try:
        source = email_user
        msg = MIMEText(message, "plain")
        msg["From"] = source
        msg["To"] = destinataire
        msg['Cc'] = email_cc
        msg["Subject"] = sujet
        server = smtplib.SMTP(email_host, email_port)
        server.connect(email_host, email_port)
        server.login(source, email_password)
        server.sendmail(source, [destinataire, source], msg.as_string())
        server.quit()
    except Exception as e:
        colour_print(f"An error occurred: {e}", 'error')
        colour_print(f"Email not sent to {destinataire}", 'error')
        return None


def main(emails_list):
    colour_print("Sending emails", 'warning')
    user_pass = parameters.get_parameter("PASSWORDS")
    pbar = tqdm.tqdm(total=len(emails_list), desc='Sending Emails', unit='email')
    for pair in user_pass:
        if pair['Email'] in emails_list:
            with open(message_file, 'r') as file:
                message = file.read()
                message = message.format(**pair)
            send_mail(pair['Email'], "Changement du mot de passe", message)
            pbar.write(f"Email sent to {pair['Email']}")
            pbar.update(1)
    pbar.close()
    colour_print("All emails have been sent", 'success')
