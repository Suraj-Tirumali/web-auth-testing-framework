"""
Module: auth_collector

Collect authentication-related artifacts from the browser context.

This module extracts information that may be used for authentication
or session management, including:

- Cookies
- localStorage data
- sessionStorage data
- HTTP headers (placeholder for future implementation)

These artifacts are later analyzed by the security analysis modules.
"""

def collect_auth_data(context):
    """
    Collect authentication artifacts from the Playwright browser context.

    Parameters:
        context: Playwright browser context object

    Returns:
        dict containing:
            cookies: list of browser cookies
            storage: localStorage and sessionStorage contents
            headers: placeholder list for HTTP headers
    """

    # Extract cookies stored by the browser session
    cookies = context.cookies()

    # Initialize storage containers
    storage_data = {
        "localStorage": {},
        "sessionStorage": {}
    }

    # Get all open pages in the browser context
    pages = context.pages

    # If at least one page exists, use the latest page
    if pages:
        page = pages[-1]

        try:
            # Extract all key/value pairs from localStorage
            local_storage = page.evaluate("""
                () => {
                    let data = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        let key = localStorage.key(i);
                        data[key] = localStorage.getItem(key);
                    }
                    return data;
                }
            """)

            # Extract all key/value pairs from sessionStorage
            session_storage = page.evaluate("""
                () => {
                    let data = {};
                    for (let i = 0; i < sessionStorage.length; i++) {
                        let key = sessionStorage.key(i);
                        data[key] = sessionStorage.getItem(key);
                    }
                    return data;
                }
            """)

            storage_data["localStorage"] = local_storage
            storage_data["sessionStorage"] = session_storage

        except Exception as e:
            # Storage extraction may fail on some sites (e.g., cross-origin)
            print(f"[WARNING] Storage extraction failed: {e}")

    # Placeholder for HTTP header extraction
    headers = []

    return {
        "cookies": cookies,
        "storage": storage_data,
        "headers": headers
    }