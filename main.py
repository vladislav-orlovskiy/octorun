#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################`
# @file    : main.py
# @author  : Uladzislau Orlovskiy
# @email   : painanguishagony@gmail.com`
# @date    : 2023-10-01
# @brief   : Main entry point for the application.
################################################################################

import logging

import octorun.webhook_listener.app as webhook_listener
from octorun.Classes import Config


def main():
    logging.info("Loading config")
    config = Config.load()
    logging.getLogger().setLevel(config.logging_level)
    logging.info("Config loaded. Starting webhook listener")
    webhook_listener.start(
        webhook_path=config,
        webhook_secret=config.webhook_secret,
        github_app_installation_id=config.github_app_installation_id,
        github_app_private_key=config.github_app_private_key,
        ca_cert=config.get_ca_crt(),
        cert=config.get_crt(),
        private_key_path=config.private_key_path,
        port=443,
        debug=False,
    )


if __name__ == "__main__":
    main()
