import time

import jwt
import requests


def get_gh_app_token(gh_app_id: str, gh_app_key: str) -> str:
    """
    Get the GitHub App token.
    :param gh_app_id: The GitHub App ID.
    :param gh_app_key: The GitHub App key.
    :return: The GitHub App token.
    """
    now = int(time.time())
    payload = {"iat": now, "exp": now + 60 * 10, "iss": gh_app_id}
    return jwt.encode(payload, gh_app_key, algorithm="RS256")


def get_gh_runner_registration_token(gh_app_token: str, owner: str) -> str:
    """
    Get the GitHub runner registration token.
    :param gh_app_token: The GitHub App token.
    :param owner: The owner of the repository.
    :return: The GitHub runner registration token.
    """
    url = f"https://api.github.com/orgs/{owner}/actions/runners/registration-token"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gh_app_token}",
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Failed to get runner registration token: {response.text}")
    return response.json()["token"]


def get_labels_from_webhook(payload: str) -> list:
    """
    Process the GitHub webhook payload.
    :param payload: The GitHub webhook payload.
    :return: list of labels.
    """
    labels = []
    workflow_name = payload.get("workflow_run", {}).get("name")
    repo_name = payload.get("repository", {}).get("full_name")
    print(f"Workflow '{workflow_name}' triggered in repo '{repo_name}'.")

    # Check for issues linked via workflow run if any
    # (usually not directly available from workflow_run)
    return labels
