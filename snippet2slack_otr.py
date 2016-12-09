#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Docstring """

import json
import requests
import logging
from datetime import datetime, timedelta

# pylint: disable=invalid-name,global-statement

CONFIG_FILE = "config.json"
SAVE_CONFIG = True
message = ""
Start = 0

def save_json(f, cfg):
    """ Save JSON-formatted file """
    try:
        with open(f, 'w') as configfile:
            json.dump(cfg, configfile)
    except:
        return False
    return True

def read_json(f):
    """ Read JSON-formatted file """
    data = []
    try:
        with open(f, 'r') as configfile:
            data = json.load(configfile)
    except (FileNotFoundError, PermissionError):
        pass
    return data

def default_json(flag):
    if flag is 'config':
        return {"token": "", "filepath": "", "slack-channel": "#webhook-test"}
    else:
        return {}

def send_file(slacktoken, filepath, slackchannel):
    """ Docstring """

    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    file = filepath + "" + yesterday + ".log"
    options = {
        "token": slacktoken,
        "content": open(file, 'rb').read(),
        "title": "Chatlog " + yesterday,
        "channels": slackchannel
    }
    requests.post("https://slack.com/api/files.upload", options)


logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO,
                    filename='file.log',
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

CONFIG = read_json(CONFIG_FILE)
if not CONFIG:
    CONFIG = default_json('config')
    if SAVE_CONFIG is True:
        save_json(CONFIG_FILE, CONFIG)

if (Start == 0):
    logger.info("Started!")
    send_file(CONFIG["token"], CONFIG["filepath"], CONFIG["slack-channel"])
    Start = 1
    logger.info("Done!")
