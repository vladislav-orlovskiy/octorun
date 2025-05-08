import logging
import socket
from urllib.parse import urlparse

import config
import rpyc
import utils

import octorun.utils as utils


class Provider:
    def __init__(self, name, socket, labels, org):
        self.name = name
        self.socket = socket
        self.labels = labels
        self.org = org

    def connect_to_provider(self):
        """
        This function is used to connect to the provider.
        :return: The connection object.
        """
        try:
            logging.info(f"Connecting to provider {self.name}")
            parsed_socket = urlparse(self.socket)
            if parsed_socket.scheme == "tcp":
                connection = rpyc.connect(parsed_socket.hostname, parsed_socket.port)
                logging.info("Connected to provider")
                return connection
            elif parsed_socket.scheme == "unix":
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(parsed_socket.path)
                connection = rpyc.connect_stream(sock.makefile("rwb"))
                logging.info("Connected to provider")
                return connection
            else:
                logging.error(f"Unsupported socket scheme: {parsed_socket.scheme}")
                return None
        except Exception as e:
            logging.error(f"Error connecting to provider: {e}")
            return None

    def get_github_runner_token(self):
        return utils.get_github_runner_token(
            github_app_installation_id=config.Config.github_app_installation_id,
            github_app_private_key=config.Config.github_app_private_key,
            org=self.org,
        )

    def request_runner(self):
        """
        This function is used to request the runner.
        :return: The response of the request.
        """
        try:
            logging.info(f"Requesting runner from provider {self.name}")
            connection = self.connect_to_provider()
            if connection is None:
                error_message = f"Unable to connect to provider {self.name}"
                logging.error(error_message)
                return error_message
            # Send the request to the provider
            response = connection.root.exposed_request_runner(
                labels=str(self.labels),
                gh_runner_token=self.get_github_runner_token(),
                org=self.org,
            )
            logging.info(f"Received response from provider: {response}")
            return response
        except Exception as e:
            logging.error(f"Error requesting runner: {e}")
            return None
