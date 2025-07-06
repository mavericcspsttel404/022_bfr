from typing import Any, Optional

import requests

from settings import SPIKE_ALERT_TITLE, SPIKE_ALERT_WEBHOOK


def create_spike_incident(
    message: str,
    name: str,
    step_id: str,
    stack: str,
    severity: Optional[str] = "sev2",
    priority: Optional[str] = "p2",
    title: str = SPIKE_ALERT_TITLE,
    webhook_url: str = SPIKE_ALERT_WEBHOOK,  # type: ignore
) -> dict[str, Any]:
    """
    Create an incident in Spike using webhook integration.

    Args:
        webhook_url (str): The complete webhook URL including the token
        title (str): Title of the incident (required)
        message (str): Message to include in incident details
        name (str): Name associated with the incident
        step_id (str): Step ID for the incident
        severity (str, optional): Incident severity (sev1, sev2, or sev3)
        priority (str, optional): Incident priority (p1, p2, p3, p4, or p5)

    Returns:
        dict: Response from the Spike API

    Raises:
        requests.exceptions.RequestException: If the request fails
    """

    # Construct the request body
    payload = {
        "title": title,
        "body": {
            "message": message,
            "name": name,
            "step_id": step_id,
            "stack": stack,
        },
    }

    # Add optional parameters if provided
    if severity and severity in ["sev1", "sev2", "sev3"]:
        payload["severity"] = severity

    if priority and priority in ["p1", "p2", "p3", "p4", "p5"]:
        payload["priority"] = priority

    if stack:
        payload["body"]["stack"] = stack

    # Make the POST request
    response = requests.post(
        webhook_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        verify=False,
    )

    # Raise an exception for bad status codes
    response.raise_for_status()

    return response.json()
