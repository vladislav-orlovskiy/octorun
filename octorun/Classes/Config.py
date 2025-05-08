import logging
import os
import secrets
from dataclasses import dataclass
from typing import Optional, Self

import yaml

from octorun.Classes.Provider import Provider


@dataclass
class Config:
    """Class for storing configuration of the application."""

    name: str
    version: str
    logging_level: Optional[str] = "ERROR"
    webhook_secret: Optional[str] = secrets.token_hex(16)
    webhook_listen_port: int = 8080
    webhook_path: str = "/webhook"
    ca_crt_path: Optional[str] = None
    cert_path: Optional[str] = None
    cert_key_path: Optional[str] = None
    github_app_installation_id: int
    github_app_private_key: str
    labels_to_listen: Optional[list[str]] = ["self-hosted"]
    providers: Optional[list[Provider]] = []

    @classmethod
    def load(cls, config_path: str) -> Self:
        """
        This function is used to initialize the config.
        :return: The config object.
        """
        logging.info("Initializing config file")
        with open("config.yaml", "r") as f:
            try:
                config_yaml = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(f"Error loading config file: {e} exiting.")
                exit(1)
        logging.info("Loading mandatory environment variables")
        try:
            cls.github_app_installation_id = os.environ.get(
                "OCTORUN_GITHUB_APP_INSTALLATION_ID"
            )
            cls.github_app_private_key = os.environ.get(
                "OCTORUN_GITHUB_APP_PRIVATE_KEY"
            )
        except KeyError as e:
            logging.error(
                f"Environment variable {e} not set. Unable to proceed. Exiting."
            )
            exit(1)

        webhook_secret = os.environ.get("OCTORUN_WEBHOOK_SECRET", None)
        if webhook_secret is None:
            logging.warning(
                f"Environment variable {webhook_secret} not set. Generating random secret. Use for evaluation purpose only!"
            )
        cls.logging = config_yaml.os.environ.get("OCTORUN_LOGGING_LEVEL", "ERROR")
        cls.name = config_yaml.get(
            "name", os.environ.get("OCTORUN_APP_NAME", "octorun")
        )
        cls.org = config_yaml.get("github", {}).get(
            "org", os.environ.get("OCTORUN_ORG_NAME", None)
        )
        cls.webhook_listen_port = os.environ.get("OCTORUN_WEBHOOK_PORT", 8080)
        cls.webhook_path = os.environ.get("OCTORUN_WEBHOOK_PATH", "/webhook")
        return cls

    @staticmethod
    def _get_cert_file(path: str) -> Optional[str]:
        """
        This function is used to get the certificate file.
        :return: The certificate file.
        """
        if path is None:
            return None
        if not os.path.exists(path):
            logging.error(
                f"Certificate file {path} not found. Unable to proceed. Exiting."
            )
            return None
        return path
