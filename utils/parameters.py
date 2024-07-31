from utils.coloration import colour_print


def load_dotenv(file_path):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars


def show_env_variables(file_path):
    env_vars = load_dotenv(file_path)
    for key, value in env_vars.items():
        colour_print(f"{key}: {value}", 'info')
    print()


def show_domaines():
    domaines = get_parameter("DOMAINES")
    for domain in domaines:
        colour_print(domain, 'info')
    print()


def get_parameter(type_parameter):
    from dotenv import load_dotenv
    import os
    parameter_list = []
    load_dotenv("envs/.static.env")
    parameter = os.getenv(type_parameter)
    with open(parameter, 'r') as file:
        if parameter.endswith('.txt'):
            extract_txt_lines(parameter_list, file)
        elif parameter.endswith('.csv'):
            extract_csv_lines(parameter_list, file)
    return parameter_list


def extract_txt_lines(parameter_list, file):
    for line in file:
        parameter_list.append(line.strip())


def extract_csv_lines(parameter_list, file):
    import csv
    reader = csv.DictReader(file)
    for row in reader:
        parameter_list.append(row)
