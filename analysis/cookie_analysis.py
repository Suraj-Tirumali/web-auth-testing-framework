"""
Module: cookie_analysis

Analyze browser cookies for common security misconfigurations.

This module checks cookies for important security attributes
that protect user sessions, including:

- HttpOnly flag
- Secure flag
- SameSite policy

Missing security flags may expose applications to attacks such as:
- Cross-Site Scripting (XSS)
- Session hijacking
- Cross-Site Request Forgery (CSRF)
"""

def analyze_cookies(cookies):
    """
    Analyze cookies for security flags and potential issues.

    Parameters:
        cookies (list): List of cookie objects collected from the browser

    Returns:
        dict containing:
            total_cookies: number of cookies found
            missing_httpOnly: cookies lacking HttpOnly flag
            missing_secure: cookies lacking Secure flag
            cookies: detailed cookie metadata
    """

    # Initialize cookie analysis report
    report = {
        "total_cookies": len(cookies),
        "missing_httpOnly": [],
        "missing_secure": [],
        "cookies": []
    }

    # Iterate through all cookies collected from the browser
    for cookie in cookies:

        # Extract relevant cookie attributes
        cookie_info = {
            "name": cookie.get("name"),
            "domain": cookie.get("domain"),
            "httpOnly": cookie.get("httpOnly", False),
            "secure": cookie.get("secure", False),
            "sameSite": cookie.get("sameSite", "None")
        }

        # Store cookie metadata
        report["cookies"].append(cookie_info)

        # Check for missing HttpOnly flag (protects against XSS)
        if not cookie_info["httpOnly"] and cookie_info["name"]:
            report["missing_httpOnly"].append(cookie_info["name"])

        # Check for missing Secure flag (ensures HTTPS transmission)
        if not cookie_info["secure"] and cookie_info["name"]:
            report["missing_secure"].append(cookie_info["name"])

    return report