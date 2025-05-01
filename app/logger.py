import logging
import os

LOG_FILE = os.path.expanduser("~/.local/share/pyIDevicesGUI/app.log")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

def info(msg):
    logging.info(msg)

def warning(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)

def debug(msg):
    logging.debug(msg)

print(f"📝 Log gravado em: {LOG_FILE}")
