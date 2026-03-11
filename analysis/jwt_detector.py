"""
Module: jwt_detector

Detect JSON Web Tokens (JWT) stored in browser storage.

JWT tokens are commonly used for authentication in modern web
applications and APIs. They are typically stored in:

- localStorage
- sessionStorage

This module scans browser storage values and identifies strings
that match the standard JWT structure.
"""

import re


# Regex pattern for detecting JWT tokens
# JWT format: header.payload.signature
JWT_PATTERN = re.compile(r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$")


def detect_jwt(storage_data):
    """
    Detect JWT tokens inside browser storage.

    Parameters:
        storage_data (dict): Dictionary containing localStorage
                             and sessionStorage contents

    Returns:
        list of detected JWT tokens with metadata
    """

    detected_tokens = []

    # Check both localStorage and sessionStorage
    for storage_type in ["localStorage", "sessionStorage"]:

        storage = storage_data.get(storage_type, {})

        # Iterate through storage key/value pairs
        for key, value in storage.items():

            # Check if the value matches the JWT pattern
            if isinstance(value, str) and JWT_PATTERN.search(value):

                detected_tokens.append({
                    "storage": storage_type,
                    "key": key,
                    "token": value
                })

    return detected_tokens