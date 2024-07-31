#!.venv/bin/python3
from utils import get_mails, generate_passwords, parameters, create_user, alert_users, menu
from utils.system_state import check_system, update_system
from utils.coloration import colour_print


QUITTER = "[q] Quitter"


def files_checks():
    # check if the .env files exist
    if not parameters.check_env_files():
        colour_print("Les fichiers de configuration n'existent pas, veuillez les créer.", 'error')
        return False


def show_infos():
    while True:
        options = ["[s] SSH",
                   "[f] Static",
                   "[@] Domaines",
                   QUITTER
                   ]
        _, menu_entry_index = menu.create_terminal_menu(options, "Informations")
        match menu_entry_index:
            case 0:
                parameters.show_env_variables("envs/.ssh.env")
            case 1:
                parameters.show_env_variables("envs/.static.env")
            case 2:
                parameters.show_domaines()
            case _:
                break


def parameters_menu():
    while True:
        options = ["[e] Editer paramètres",
                   "[c] Effacer toute les informations",
                   "[v] Visualiser informations",
                   QUITTER
                   ]
        _, menu_entry_index = menu.create_terminal_menu(options, "Paramètres")
        match menu_entry_index:
            case 0:
                print("Editer paramètres")
            case 1:
                print("Effacer toute les informations")
            case 2:
                show_infos()
            case _:
                break


def check_domaines():
    options = parameters.get_parameter("DOMAINES")
    terminal_menu, _ = menu.create_terminal_menu(options, multi_select=True, preselected_entries=options, titre="Domaines à vérifier")
    domaines = terminal_menu.chosen_menu_entries
    if domaines is None or len(domaines) == 0:
        return

    get_mails.main(domaines)
    update_system("mails_retrieved")


def check_mail_spam_settings():
    options = parameters.get_parameter("EMAILS")
    terminal_menu, _ = menu.create_terminal_menu(options, multi_select=True, preselected_entries=options, titre="Utilisateurs à avertir du changement")
    utilisateurs = terminal_menu.chosen_menu_entries
    if utilisateurs is None or len(utilisateurs) == 0:
        return

    alert_users.main(utilisateurs)


def creates_users_settings():
    options = parameters.get_parameter("EMAILS")
    terminal_menu, _ = menu.create_terminal_menu(options, multi_select=True, preselected_entries=options, titre="Utilisateurs à créer")
    utilisateurs = terminal_menu.chosen_menu_entries
    if utilisateurs is None or len(utilisateurs) == 0:
        return

    create_password = validate_choice("Voulez-vous générer des mots de passes pour les utilisateurs ?", annuler=True)
    if create_password is None:
        return

    create_user.main(utilisateurs, create_password)
    update_system("user_created")


def validate_choice(titre, annuler=False):
    options = ["[o] Oui", "[n] Non"]
    if annuler:
        options.append("[q] Annuler")
    _, menu_entry_index = menu.create_terminal_menu(options, titre=titre)
    if menu_entry_index == 0:
        return True
    elif menu_entry_index == 1:
        return False
    else:
        return None


def main():
    options = ["[r] Récuperation mails",
               "[g] Génération mots de passes",
               "[m] Alerter utilisateurs par mail",
               "[c] Creation de comptes",
               "[s] Changer les mots de passe sur le serveur source",
               "[p] Paramètres",
               QUITTER
               ]
    while True:
        _, menu_entry_index = menu.create_terminal_menu(options, "Menu Principal")

        match menu_entry_index:
            case 0:
                if check_system("mails_retrieved"):
                    if validate_choice("Une liste de mails a déjà été récupérée, voulez-vous la supprimer et en récupérer une nouvelle ?"):
                        check_domaines()
                else:
                    check_domaines()
            case 1:
                if check_system("passwords_generated"):
                    if validate_choice("Il y a déjà des mots de passes générés pour votre liste de mails, voulez-vous les regénérer ?"):
                        generate_passwords.main()
                else:
                    generate_passwords.main()
                update_system("passwords_generated")
            case 2:
                check_mail_spam_settings()
            case 3:
                if check_system("user_created"):
                    if validate_choice("Il semble que des utilisateurs aient déjà été créés, voulez-vous quand même continuer ?"):
                        creates_users_settings()
                else:
                    creates_users_settings()
            case 4:
                print("changer mdp source")
            case 5:
                parameters_menu()
            case _:
                break


if __name__ == "__main__":
    main()
