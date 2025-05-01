import configparser
import os

CONFIG_PATH = os.path.expanduser("~/.config/pyIDevicesGUI/config.ini")

config = configparser.ConfigParser()

# Carrega config, cria se não existir
if not os.path.exists(CONFIG_PATH):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        f.write("[geral]\nbackup_path=\n")

config.read(CONFIG_PATH)

def get_backup_path():
    return config.get("geral", "backup_path", fallback="")

def set_backup_path(path):
    config.set("geral", "backup_path", path)
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)
