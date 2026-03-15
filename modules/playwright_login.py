"""
Module: playwright_login

Handles automated login using Playwright.

This module attempts to:
1. Launch a Chromium browser
2. Detect common username/password fields
3. Submit login credentials
4. Handle potential MFA/CAPTCHA interruptions
5. Capture a screenshot of the login result

The browser context is returned so authentication artifacts
(cookies, storage, etc.) can be collected by the framework.
"""

from playwright.sync_api import sync_playwright
import os
from core.output_manager import prepare_output


def playwright_login(url, username, password):
    """
    Perform automated login using Playwright.

    Parameters:
        url (str): Login page URL
        username (str): Username credential
        password (str): Password credential

    Returns:
        context: Playwright browser context
        screenshot_path: Path to captured screenshot
        success (bool): Login success status
        output_dir: Directory where artifacts are stored
    """

    # Start Playwright and launch a visible Chromium browser
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

    # Create browser context and page
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the login page
    page.goto(url)

    # Wait until the page finishes loading network activity
    page.wait_for_load_state("networkidle")

    # Common selectors used by websites for username/email fields
    username_selectors = [
        "input[name='username']",
        "input[name='email']",
        "input[type='email']",
        "#username",
        "#email"
    ]

    # Common selectors for password fields
    password_selectors = [
        "input[name='password']",
        "input[type='password']",
        "#password"
    ]

    # Possible selectors for login/submit buttons
    login_button_selectors = [
        "button[type='submit']",
        "button:has-text('Login')",
        "button:has-text('Log in')",
        "button:has-text('Sign In')",
        "button:has-text('Continue')",
        "input[type='submit']"
    ]

    username_field = None
    password_field = None
    login_button = None

    # Attempt to locate username field using known selectors
    for selector in username_selectors:
        try:
            username_field = page.query_selector(selector)
            if username_field:
                break
        except:
            pass

    # Attempt to locate password field
    for selector in password_selectors:
        try:
            password_field = page.query_selector(selector)
            if password_field:
                break
        except:
            pass

    # Attempt to locate login button
    for selector in login_button_selectors:
        try:
            login_button = page.query_selector(selector)
            if login_button:
                break
        except:
            pass

    # If required fields are missing, automated login cannot proceed
    if not username_field or not password_field:
        raise Exception("Login fields not found")

    # Fill credentials into detected input fields
    username_field.fill(username)
    password_field.fill(password)

    # Click login button if found
    if login_button:
        login_button.click()

    # Allow time for login redirect or verification page
    page.wait_for_timeout(5000)

    # If URL did not change, login may require additional verification
    if page.url == url:
        print("\n[INFO] Login may require additional verification (MFA / CAPTCHA).")
        print("Please complete the verification in the browser window.")

        # Pause execution until user confirms verification is complete
        input("Press ENTER here after completing verification...")

    # Prepare output directory for this run
    output_dir, domain, timestamp = prepare_output(url)

    # Determine login success by checking URL change
    success = page.url != url

    # Choose screenshot filename based on login status
    if success:
        screenshot_name = "login_success.png"
    else:
        screenshot_name = "login_failure.png"

    screenshot_path = os.path.join(output_dir, screenshot_name)

    # Capture screenshot of the final page state
    page.screenshot(path=screenshot_path, full_page=True)

    # Close browser resources
    browser.close()
    playwright.stop()

    return context, screenshot_path, success, output_dir
