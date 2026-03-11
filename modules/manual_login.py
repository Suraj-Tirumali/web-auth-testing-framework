"""
Module: manual_login

Handles manual authentication flows that cannot be automated.

This module launches a visible browser and allows the user to
complete login manually. This is useful for scenarios such as:

- Multi-Factor Authentication (MFA)
- CAPTCHA challenges
- OAuth / SSO authentication
- Device verification

After the user confirms login completion, a screenshot is captured
and the browser context is returned for artifact collection.
"""

from playwright.sync_api import sync_playwright
import os
from core.output_manager import prepare_output


def manual_login(url):
    """
    Perform manual login by allowing the user to interact with the browser.

    Parameters:
        url (str): Login page URL

    Returns:
        context: Playwright browser context
        screenshot_path: Path to captured screenshot
        success (bool): Assumed login status
        output_dir: Directory where artifacts are stored
    """

    # Start Playwright and launch a visible browser
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

    # Create browser context and page
    context = browser.new_context()
    page = context.new_page()

    # Navigate to login page
    page.goto(url)

    # Wait until page finishes loading
    page.wait_for_load_state("networkidle")

    print("\nManual login mode enabled.")
    print("Please complete the login process in the opened browser window.")
    print("Leave the browser open.")
    print("Then press ENTER here to continue analysis.")

    # Pause script execution until user confirms login completion
    input("\nPress ENTER here AFTER completing login...\n")

    # Prepare output directory for this run
    output_dir, domain, timestamp = prepare_output(url)

    # Manual login assumes success; screenshot will show final state
    screenshot_path = os.path.join(output_dir, "login_success.png")

    # Capture screenshot of current browser state
    page.screenshot(path=screenshot_path, full_page=True)

    return context, screenshot_path, True, output_dir