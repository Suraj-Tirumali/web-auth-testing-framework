"""
Module: header_analysis

Analyze HTTP headers for authentication-related information.

This module focuses on detecting authorization headers and
Bearer tokens that may be used for API authentication.

Bearer tokens are commonly used in modern applications for:
- JWT authentication
- OAuth authentication
- API access control
"""

import re


# Regex pattern to detect Bearer tokens in headers
BEARER_PATTERN = re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE)


def analyze_headers(headers):
    """
    Analyze HTTP headers for authentication tokens.

    Parameters:
        headers (list): List of HTTP header objects

    Returns:
        dict containing:
            authorization_headers: detected Authorization header values
            bearer_tokens: detected Bearer tokens
    """

    # Initialize analysis report
    report = {
        "authorization_headers": [],
        "bearer_tokens": []
    }

    # Iterate through collected headers
    for header in headers:

        name = header.get("header", "").lower()
        value = header.get("value", "")

        # Detect Authorization headers
        if name == "authorization":
            report["authorization_headers"].append(value)

        # Detect Bearer tokens using regex pattern
        if BEARER_PATTERN.search(value):
            if value in report["bearer_tokens"]:
                report["bearer_tokens"].append(value)

    return report
