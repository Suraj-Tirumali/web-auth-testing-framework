"""
Module: output_manager

Manage output directories and artifact storage for the framework.

Each test run generates a structured output directory that contains:
- login screenshots
- analysis results (results.json)

Directory structure:

outputs/
   domain_name/
      run_timestamp/
         login_success.png
         results.json
"""

import os
from urllib.parse import urlparse
from datetime import datetime


def prepare_output(url):
    """
    Create a structured output directory for a test run.

    Parameters:
        url (str): Target login URL

    Returns:
        output_dir (str): Full path to the run directory
        domain (str): Sanitized domain name
        timestamp (str): Timestamp identifier for the run
    """

    # Parse domain from URL
    parsed = urlparse(url)

    # Convert domain into filesystem-friendly format
    domain = parsed.netloc.replace(".", "_")

    # Generate timestamp for the test run
    timestamp = datetime.now().strftime("run_%Y_%m_%d_%H_%M_%S")

    # Construct output directory path
    output_dir = os.path.join("outputs", domain, timestamp)

    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    return output_dir, domain, timestamp


def save_placeholder_screenshot(output_dir, status="success"):
    """
    Generate a placeholder screenshot file.

    This is used for login methods that do not use a browser
    (e.g., API-based authentication).

    Parameters:
        output_dir (str): Directory where the file will be saved
        status (str): Login status indicator

    Returns:
        path (str): Path to the placeholder file
    """

    filename = f"login_{status}.png"

    path = os.path.join(output_dir, filename)

    # Create placeholder file explaining screenshot absence
    with open(path, "w") as f:
        f.write("Screenshot not available for this login method")

    return path