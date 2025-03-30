# youtrack_api.py - Functions for interacting with YouTrack API

import requests
import os

# Configuration - Consider moving to a config file or environment variables
YOUTRACK_URL = os.environ.get("YOUTRACK_URL", "YOUR_YOUTRACK_INSTANCE_URL") # e.g., "https://yourcompany.youtrack.cloud"
YOUTRACK_TOKEN = os.environ.get("YOUTRACK_TOKEN", "YOUR_YOUTRACK_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {YOUTRACK_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# --- Placeholder Functions --- #

def search_issues(query: str, fields: str = "idReadable,summary,project(shortName)", custom_fields: str = None, top: int = 100, skip: int = 0):
    """
    Search for issues in YouTrack using a query.

    Args:
        query (str): The search query string (YouTrack query syntax).
        fields (str): Comma-separated list of fields to return for each issue.
                      Defaults to "idReadable,summary,project(shortName)".
        custom_fields (str, optional): Comma-separated list of custom fields to include.
        top (int): The maximum number of issues to return. Defaults to 100.
        skip (int): The number of issues to skip from the beginning of the results. Defaults to 0.

    Returns:
        list or dict: A list of found issues or an error dictionary.
    """
    endpoint = "issues"
    params = {
        "query": query,
        "fields": fields,
        "$top": top,
        "$skip": skip,
    }
    if custom_fields:
        # Ensure custom fields are added correctly to the main fields parameter
        params["fields"] += f",{custom_fields}"

    print(f"Searching YouTrack issues with query: '{query}'...") # Keep a print for visibility
    return _make_request("GET", endpoint, params=params)

def get_issue(issue_id: str, fields: str = "idReadable,summary,description,project(shortName),customFields(projectCustomField(field(name)),value(name,login,fullName,text))", custom_fields: str = None):
    """
    Get details for a specific YouTrack issue by its ID.

    Args:
        issue_id (str): The ID of the issue (e.g., "PROJ-123").
        fields (str): Comma-separated list of fields to return for the issue.
                      Defaults to a comprehensive set including common fields and custom fields.
        custom_fields (str, optional): Additional comma-separated list of custom fields to explicitly include
                                     (useful if the default 'fields' doesn't cover specific needs).

    Returns:
        dict: A dictionary containing the issue details or an error dictionary.
    """
    endpoint = f"issues/{issue_id}"
    params = {"fields": fields}
    if custom_fields:
        # Append custom fields if they are specified separately
        params["fields"] += f",{custom_fields}"

    print(f"Getting details for YouTrack issue: {issue_id}...")
    return _make_request("GET", endpoint, params=params)

def update_issue(issue_id: str, data: dict, fields: str = "idReadable,summary"):
    """
    Update an existing YouTrack issue by its ID.

    Args:
        issue_id (str): The ID of the issue to update (e.g., "PROJ-123").
        data (dict): A dictionary containing the fields to update and their new values.
                     Example: {"summary": "New summary", "description": "Updated description"}
                     For custom fields, use their name as the key and a dict with the value type, e.g.:
                     {"Custom Field Name": {"name": "New Value"}} for Enum types,
                     {"Custom User Field": {"login": "user.login"}} for User types.
        fields (str): Comma-separated list of fields to return for the updated issue.
                      Defaults to "idReadable,summary".

    Returns:
        dict: A dictionary containing the specified fields of the updated issue or an error dictionary.
    """
    endpoint = f"issues/{issue_id}"
    params = {"fields": fields}
    print(f"Updating YouTrack issue {issue_id} with data: {data}...")
    # Use POST method and pass data in the json parameter
    return _make_request("POST", endpoint, params=params, json_data=data)

def add_comment(issue_id: str, comment_text: str, fields: str = "id,text,author(login)"):
    """
    Add a comment to a YouTrack issue.

    Args:
        issue_id (str): The ID of the issue to comment on (e.g., "PROJ-123").
        comment_text (str): The text content of the comment.
        fields (str): Comma-separated list of fields to return for the created comment.
                      Defaults to "id,text,author(login)".

    Returns:
        dict: A dictionary containing the specified fields of the created comment or an error dictionary.
    """
    endpoint = f"issues/{issue_id}/comments"
    params = {"fields": fields}
    json_data = {"text": comment_text}
    print(f"Adding comment to YouTrack issue {issue_id}: '{comment_text[:50]}...'")
    return _make_request("POST", endpoint, params=params, json_data=json_data)

# --- Helper Function --- #

def _make_request(method, endpoint, params=None, json_data=None):
    """Helper function to make requests to the YouTrack API."""
    url = f"{YOUTRACK_URL}/api/{endpoint}"
    try:
        response = requests.request(method, url, headers=HEADERS, params=params, json=json_data)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        # Handle cases where response might be empty (e.g., 204 No Content)
        if response.status_code == 204:
            return {}
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        # Consider more robust error handling/logging
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred"}

# Example usage (for testing purposes)
if __name__ == "__main__":
    if YOUTRACK_URL == "YOUR_YOUTRACK_INSTANCE_URL" or YOUTRACK_TOKEN == "YOUR_YOUTRACK_PERMANENT_TOKEN":
        print("Please set YOUTRACK_URL and YOUTRACK_TOKEN environment variables or update them in youtrack_api.py")
    else:
        # Example: Get details for a specific issue
        issue_id_to_test = "FXS-1673"
        print(f"\nAttempting to get details for issue: {issue_id_to_test}...")
        issue_details = get_issue(issue_id_to_test)

        if isinstance(issue_details, dict) and 'error' not in issue_details:
            print(f"\n--- Details for {issue_details.get('idReadable', 'N/A')} ---")
            print(f"  Summary: {issue_details.get('summary', 'N/A')}")
            print(f"  Project: {issue_details.get('project', {}).get('shortName', 'N/A')}")
            # Optionally print description or other fields if needed
            # print(f"  Description: {issue_details.get('description', 'N/A')}")
            print("--- End Details ---")
        else:
            print(f"\nError getting issue details for {issue_id_to_test}: {issue_details}")

        # You can add calls to other functions like search_issues here for further testing
        # print("\nSearching for issues...")
        # search_results = search_issues("project: YourProject state: Open", top=5)
        # # ... (handle search results as before)
