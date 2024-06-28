"""
Module: Power BI Page Configuration Updater

This module retrieves pages from a specified Power BI report and updates a SQL table with the page configuration.
It utilizes Azure AD for authentication and interacts with the Power BI REST API to fetch the page details.

Environment Variables:
- AZURE_CLIENT_ID: The client ID for Azure AD authentication.
- AZURE_CLIENT_SECRET: The client secret for Azure AD authentication.
- AZURE_TENANT_ID: The tenant ID for Azure AD authentication.
- WORKSPACE_ID: The Power BI workspace ID containing the report.
- REPORT_ID: The Power BI report ID from which to retrieve the pages.

Constants:
- PAGES_CONFIG_TABLE: The name of the SQL table to store the Power BI pages configuration.

Functions:
- main(): The main entry point of the script, which retrieves the page data and updates the SQL table.

Dependencies:
- os: Provides functions for interacting with the operating system, used for environment variable access.
- pandas: Used for data manipulation and DataFrame operations.
- pbi: Custom module containing functions for Power BI API interactions (get_access_token, list_pages) and the ReportInstance namedtuple.
- sql: Custom module providing a database connection context manager.

Example usage:
    Run the script as a standalone module to update the Power BI pages configuration in the SQL table:
    ```
    python main.py
    ```

Module entry point:
    The script executes the main function if run as the main module.
"""
import os
import pandas as pd
from pbi import get_access_token, list_pages, ReportInstance
from sql import connection

PAGES_CONFIG_TABLE = "PBIPagesConfig"
if __name__ == "__main__":
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    tenant_id = os.environ["AZURE_TENANT_ID"]
    workspace_id = os.environ["WORKSPACE_ID"]
    report_id = os.environ["REPORT_ID"]

    report_instance = ReportInstance(
        client_id, client_secret, tenant_id, workspace_id, report_id
    )
    token = get_access_token(report_instance)
    pages = list_pages(instance=report_instance, token=token)
    page_data = pages["value"]
    page_data = pd.DataFrame(page_data)
    page_data = page_data.sort_values("order", ascending=False)
    with connection() as conn:
        page_data.to_sql(
            con=conn,
            name=PAGES_CONFIG_TABLE,
            schema="scd",
            index=False,
            if_exists="replace",
        )
