import json
import re
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        log_file = request.files["log_file"]
        if not log_file:
            return render_template("index.html", error="Please choose a log file to upload.")

        log_file_name = log_file.filename
        try:
            log_data = log_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return render_template("index.html", error="Invalid file format. Please choose a text-based log file.")

        ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        sql_keywords = ["sql", "union", "select", "insert", "update", "delete", "drop"]
        xss_keywords = ["<script>", "javascript:", "onmouseover=", "onerror="]
        port_scan_keywords = ["nmap", "masscan", "zmap", "unicornscan"]

        security_issues = {
            "SQL Injection": 0,
            "Cross-Site Scripting (XSS)": 0,
            "Port Scan": 0,
            # Add more security issues here
        }

        ip_addrs_info = {}
        total_success = 0
        total_failed = 0

        # Create a dictionary to store counts for each IP address contributing to security issues
        ip_security_counts = {}

        for log in log_data.splitlines():
            ip_match = re.search(ip_pattern, log)
            if ip_match:
                ip_address = ip_match.group()
                if ip_address not in ip_addrs_info:
                    ip_addrs_info[ip_address] = {"Success": 0, "Failed": 0}

                success_match = re.search(r"Success", log, re.I)
                failed_match = re.search(r"Failed", log, re.I)

                if success_match:
                    ip_addrs_info[ip_address]["Success"] += 1
                    total_success += 1
                elif failed_match:
                    ip_addrs_info[ip_address]["Failed"] += 1
                    total_failed += 1

                for keyword in sql_keywords:
                    if keyword in log.lower():
                        security_issues["SQL Injection"] += 1
                        # Track IP address contributing to SQL Injection count
                        if ip_address not in ip_security_counts:
                            ip_security_counts[ip_address] = {}
                        ip_security_counts[ip_address]["SQL Injection"] = ip_security_counts[ip_address].get("SQL Injection", 0) + 1

                for keyword in xss_keywords:
                    if keyword in log.lower():
                        security_issues["Cross-Site Scripting (XSS)"] += 1
                        # Track IP address contributing to XSS count
                        if ip_address not in ip_security_counts:
                            ip_security_counts[ip_address] = {}
                        ip_security_counts[ip_address]["Cross-Site Scripting (XSS)"] = ip_security_counts[ip_address].get("Cross-Site Scripting (XSS)", 0) + 1

                for keyword in port_scan_keywords:
                    if keyword in log.lower():
                        security_issues["Port Scan"] += 1
                        # Track IP address contributing to Port Scan count
                        if ip_address not in ip_security_counts:
                            ip_security_counts[ip_address] = {}
                        ip_security_counts[ip_address]["Port Scan"] = ip_security_counts[ip_address].get("Port Scan", 0) + 1

        ip_addrs_info["Total"] = {"Success": total_success, "Failed": total_failed}

        df = pd.DataFrame.from_dict(ip_addrs_info, orient="index")
        df.index.name = "IP Address"
        df.reset_index(inplace=True)

        # Convert issue names and counts to JSON for JavaScript
        issue_names = ["SQL Injection", "Cross-Site Scripting (XSS)", "Port Scan"]
        issue_counts = [
            security_issues["SQL Injection"],
            security_issues["Cross-Site Scripting (XSS)"],
            security_issues["Port Scan"]
        ]

        return render_template("index.html", df=df, security_issues=security_issues, ip_security_counts=ip_security_counts, issue_names=json.dumps(issue_names), issue_counts=json.dumps(issue_counts))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
