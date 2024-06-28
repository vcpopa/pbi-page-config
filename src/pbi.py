"""
Module: Power BI API Utilities

This module provides utility functions to interact with the Power BI REST API. It includes
functions for authenticating with Azure AD to retrieve an access token and for listing
pages of a Power BI report.

Classes and NamedTuples:
- ReportInstance: Named tuple that holds the configuration details for accessing a Power BI report.

Functions:
- get_access_token(instance: ReportInstance) -> str:
    Authenticate with Azure AD and retrieve an access token.

- list_pages(instance: ReportInstance, token: str) -> Dict[str, Any]:
    Retrieve a list of pages from a Power BI report.

Dependencies:
- requests: Used for making HTTP requests to the Power BI and Azure AD endpoints.
"""

from typing import Dict, Any
from collections import namedtuple
import requests

SCOPE = "https://analysis.windows.net/powerbi/api/.default"
ReportInstance = namedtuple(
    "ReportInstance",
    ["client_id", "client_secret", "tenant_id", "workspace_id", "report_id"],
)


def get_access_token(instance: ReportInstance) -> str:
    """
    Authenticate with Azure AD and retrieve an access token.

    Args:
    - instance (ReportInstance): The ReportInstance containing client_id, client_secret, and tenant_id.

    Returns:
    - str: The access token.
    """

    params = {
        "grant_type": "client_credentials",
        "client_id": instance.client_id,
        "client_secret": instance.client_secret,
        "scope": SCOPE,
    }
    tenant_id = instance.tenant_id
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    r = requests.post(auth_url, data=params)
    r.raise_for_status()  # Raise an exception for HTTP errors
    token = r.json()["access_token"]
    return token


def list_pages(instance: ReportInstance, token: str) -> Dict[str, Any]:  #
    """
    Retrieve a list of pages from a Power BI report.

    Args:
    - instance (ReportInstance): The ReportInstance containing workspace_id and report_id.
    - token (str): The authorization token.

    Returns:
    - Dict[str, Any]: A dictionary containing the page data.
    """
    workspace_id = instance.workspace_id
    report_id = instance.report_id
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/pages"
    headers = {
        "Authorization": f"Bearer {token}",  # Ensure token is formatted correctly
        "Content-Type": "application/json",
    }

    # Send the GET request
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    page_data = response.json()
    return page_data
