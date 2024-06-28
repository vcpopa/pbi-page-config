"""
Module: Azure KeyVault Utilities

This module provides a utility function for retrieving credentials from Azure KeyVault.

Functions:
- get_credential(name):
    Retrieves a credential value from Azure KeyVault.

Dependencies:
- azure.identity.DefaultAzureCredential: Provides a default Azure credential to authenticate.
- azure.keyvault.secrets.SecretClient: Allows interaction with Azure KeyVault to retrieve secrets.
- exc.KeyVaultError: Custom exception for handling KeyVault errors.
"""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from exc import KeyVaultError  # pylint: disable=import-error


def get_credential(name: str) -> str:
    """
    Retrieves a credential value from Azure KeyVault

    Parameters:
    name (str): The name of the credential inside KeyVault

    Returns:
    - credential (str)

    Raises:
    - KeyVaultError: If credential is not found or is empty
    """
    kv_uri = "https://qvh-keyvault.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)
    credential_value = client.get_secret(name).value
    if not credential_value:
        raise KeyVaultError("Credential value not found, please check KeyVault")
    return credential_value
