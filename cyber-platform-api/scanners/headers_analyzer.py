import requests

def scan_security_headers(target_url: str):
    """
    Fetches HTTP headers from a target URL and checks for missing security configurations.
    """
    findings = []
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    try:
        response = requests.get(target_url, timeout=5)
        headers = response.headers
        
        if "Strict-Transport-Security" not in headers:
            findings.append({
                "finding": "Missing HSTS Header",
                "severity": "High",
                "remediation": "Enable Strict-Transport-Security on the web server."
            })
            
        if "Content-Security-Policy" not in headers:
            findings.append({
                "finding": "Missing CSP Header",
                "severity": "Medium",
                "remediation": "Implement a Content-Security-Policy."
            })

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
        return {
            "target": target_url,
            "status": "error",
            "message": f"Could not reach target. Error: {str(e)}"
        }