import requests

def scan_security_headers(target_url: str):
    """
    Fetches HTTP headers from a target URL and checks for missing security configurations.
    """
    findings = []
    
    # Ensure URL has http/https
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    try:
        # Send a GET request with a 5-second timeout so it doesn't hang forever
        response = requests.get(target_url, timeout=5)
        headers = response.headers
        
        # Check 1: HSTS (Prevents downgrade attacks to HTTP)
        if "Strict-Transport-Security" not in headers:
            findings.append({
                "finding": "Missing HSTS Header",
                "severity": "High",
                "remediation": "Enable Strict-Transport-Security on the web server."
            })
            
        # Check 2: Content-Security-Policy (Prevents XSS attacks)
        if "Content-Security-Policy" not in headers:
            findings.append({
                "finding": "Missing CSP Header",
                "severity": "Medium",
                "remediation": "Implement a Content-Security-Policy."
            })

        # Check 3: Clickjacking Protection
        if "X-Frame-Options" not in headers:
            findings.append({
                "finding": "Missing X-Frame-Options",
                "severity": "Low",
                "remediation": "Add X-Frame-Options: DENY or SAMEORIGIN."
            })

        return {
            "target": target_url,
            "status": "success",
            "findings_count": len(findings),
            "findings": findings
        }

    except requests.exceptions.RequestException as e:
        # Handle connection errors gracefully
        return {
            "target": target_url,
            "status": "error",
            "message": f"Could not reach target. Error: {str(e)}"
        }