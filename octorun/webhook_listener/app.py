import logging
from typing import Optional

import utils
from flask import Flask, jsonify, request

from octorun.Classes.Provider import Provider


def start(
    providers: list[Provider],
    github_app_installation_id: str,
    github_app_private_key: str,
    webhook_secret: str,
    webhook_path: Optional[str] = "/webhook",
    port: Optional[int] = 8080,
    cert_path: Optional[str] = None,
    private_key_path: Optional[str] = None,
    debug: Optional[bool] = False,
):
    """
    Start the webhook listener server.
    :param listen_url: The URL to listen on.
    :param ca_cert: Path to the CA certificate file.
    :param cert: Path to the certificate file.
    :param private_key: Path to the private key file.
    """
    app = Flask(__name__)

    def process_request():
        """
        This function is used to parse the webhook.
        :return: The response of the request.
        """
        # Get the request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        # Process the webhook data
        logging.info(f"Received webhook: {data}")
        event = request.headers.get("X-GitHub-Event", "ping")
        if event == "ping":
            logging.info("Received ping event")
            return jsonify({"status": "success"}), 200
        elif event == "workflow_run":
            logging.info("Received workflow_run event")
            # Process the workflow_run event
            payload = request.get_json()
            labels = utils.get_labels_from_webhook(payload)
            provider = utils.get_provider_by_labels(labels, providers)
            logging.info(f"Requested runner from provider {provider.name}")
            provider.request_runner(labels=labels)

        return jsonify({"status": "success"}), 200

    app.add_url_rule(webhook_path, "webhook", process_request, methods=["POST"])
    app.run(
        debug=debug,
        port=port,
        sslcert=cert_path,
        ssl_keyfile=private_key_path,
    )
