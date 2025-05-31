import json
import webbrowser

with open("semgrep.json", encoding="utf-8") as f:
    data = json.load(f)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Semgrep Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
        h1 { color: #333; }
        li { margin-bottom: 10px; background: #fff; padding: 10px; border-left: 4px solid #d9534f; }
        strong { color: #0275d8; }
    </style>
</head>
<body>
    <h1>Semgrep Report</h1>
    <ul>
"""

for result in data.get("results", []):
    path = result.get("path", "unknown file")
    message = result["extra"].get("message", "")
    line = result["start"].get("line", "-")
    rule = result.get("check_id", "unknown rule")
    html += f"<li><strong>{path}:{line}</strong><br><em>{rule}</em><br>{message}</li>\n"

html += "</ul></body></html>"

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open("report.html")
