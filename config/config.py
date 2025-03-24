import configparser
import os
import logging

logger = logging.getLogger(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "env.ini")

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        logger.error("Config file not found at %s", CONFIG_FILE)
        raise FileNotFoundError("Configuration file missing.")
    config.read(CONFIG_FILE)
    return config

def update_config(**kwargs):
    config = load_config()
    if 'env' not in config.sections():
        config.add_section('env')
    for key, value in kwargs.items():
        config.set('env', key, str(value))
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    logger.info("Configuration updated.")
