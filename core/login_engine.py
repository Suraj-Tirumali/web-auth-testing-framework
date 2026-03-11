"""
Module: login_engine

This module contains the core controller for the Web Authentication
Testing Framework.

Responsibilities:
- Determine the appropriate login method (manual or automated)
- Execute the login process
- Collect authentication artifacts from the browser
- Run security analysis modules
- Save structured results for each test run
"""

import json
import os

from modules.playwright_login import playwright_login
from modules.manual_login import manual_login

from core.auth_collector import collect_auth_data
from core.output_manager import prepare_output

from analysis.jwt_detector import detect_jwt
from analysis.cookie_analysis import analyze_cookies
from analysis.header_analysis import analyze_headers


class LoginEngine:
    """
    Central engine responsible for orchestrating authentication testing.

    Parameters:
        url (str): Target login URL
        username (str, optional): Username for automated login
        password (str, optional): Password for automated login
    """

    def __init__(self, url, username=None, password=None):
        # Target login URL
        self.url = url

        # Credentials (optional)
        self.username = username
        self.password = password

        # Login method used for this run
        self.method = None

        # Browser context reference
        self.browser = None

        # Directory where results will be stored
        self.output_dir = None

        # Structured results object
        self.results = {
            "url": url,
            "login_status": "failed",
            "method": None,
            "cookies": [],
            "jwt_tokens": [],
            "auth_headers": [],
            "storage": {},
            "analysis": {}
        }

    def detect_login_method(self):
        """
        Determine which login strategy should be used.

        Logic:
        - If credentials are not provided → manual login
        - If credentials are provided → automated Playwright login
        """

        # No credentials provided → manual login required
        if not self.username or not self.password:
            print("[INFO] No credentials provided. Switching to manual login.")
            return "manual"

        # Credentials available → use automated login
        print("[INFO] Credentials provided. Using Playwright automation.")
        return "playwright"

    def perform_login(self, method):
        """
        Execute the selected login method.

        Returns:
            browser context for artifact extraction
        """

        if method == "playwright":

            # Perform automated login using Playwright
            context, screenshot_path, success, output_dir = playwright_login(
                self.url, self.username, self.password
            )

            # Save output directory
            self.output_dir = output_dir

            # Record screenshot location
            self.results["screenshot"] = screenshot_path

            # Record login result
            self.results["login_status"] = "success" if success else "failed"

            return context

        elif method == "manual":

            # Launch browser and allow user to login manually
            context, screenshot_path, success, output_dir = manual_login(self.url)

            self.output_dir = output_dir
            self.results["screenshot"] = screenshot_path

            # Manual login assumes success after user confirmation
            self.results["login_status"] = "success"

            return context

        else:
            raise Exception("Unknown login method")

    def collect_authentication_data(self, browser):
        """
        Extract authentication artifacts from the browser context.

        Artifacts collected:
        - cookies
        - localStorage
        - sessionStorage
        - headers (if available)
        """

        auth_data = collect_auth_data(browser)

        self.results["cookies"] = auth_data.get("cookies", [])
        self.results["auth_headers"] = auth_data.get("headers", [])
        self.results["storage"] = auth_data.get("storage", {})

    def run_analysis(self):
        """
        Execute security analysis modules on collected authentication artifacts.
        """

        # Detect JWT tokens in browser storage
        jwt_tokens = detect_jwt(self.results.get("storage", {}))

        # Analyze cookie security flags
        cookie_report = analyze_cookies(self.results["cookies"])

        # Inspect authorization headers
        header_report = analyze_headers(self.results["auth_headers"])

        self.results["jwt_tokens"] = jwt_tokens

        # Store security analysis results
        self.results["analysis"] = {
            "cookie_analysis": cookie_report,
            "header_analysis": header_report
        }

    def save_results(self):
        """
        Save the final results as a JSON report inside the run output directory.
        """

        # Ensure output directory exists
        if not self.output_dir:
            self.output_dir, domain, timestamp = prepare_output(self.url)

        output_file = os.path.join(self.output_dir, "results.json")

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=4)

        print(f"Results saved to {output_file}")

    def run(self):
        """
        Main execution pipeline for the framework.

        Steps:
        1. Detect login method
        2. Perform login
        3. Collect authentication artifacts
        4. Run security analysis
        5. Save results
        """

        try:
            print("\n[STEP] Detecting login method...")
            method = self.detect_login_method()

            self.results["method"] = method

            print(f"[STEP] Performing login using: {method}")
            browser = self.perform_login(method)

            if browser:
                print("[STEP] Collecting authentication artifacts...")

                self.browser = browser
                self.collect_authentication_data(browser)

                print("[STEP] Running security analysis...")
                self.run_analysis()

        except Exception as e:
            print(f"[ERROR] {e}")
            self.results["error"] = str(e)

        finally:
            self.save_results()