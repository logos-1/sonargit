#!/usr/bin/env python3
"""
SonarCloud to Jira Integration Script
Fetches open issues from SonarCloud and creates Jira tickets automatically
"""

import os
import sys
import json
import requests
from typing import List, Dict, Optional

# Configuration
SONAR_URL = "https://sonarcloud.io/api"
SONAR_PROJECT_KEY = "logos-1_sonargit"
JIRA_URL = "https://yjlee32333.atlassian.net"
JIRA_PROJECT_KEY = "BTS"
JIRA_ISSUE_TYPE = "버그"  # Bug in Korean

# Get credentials from environment
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")


def get_sonar_issues() -> List[Dict]:
    """Fetch open issues from SonarCloud"""
    print("🔍 Fetching issues from SonarCloud...")
    
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    
    params = {
        "componentKeys": SONAR_PROJECT_KEY,
        "statuses": "OPEN",
        "ps": 100  # Page size
    }
    
    response = requests.get(
        f"{SONAR_URL}/issues/search",
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        print(f"❌ Error fetching SonarCloud issues: {response.status_code}")
        print(response.text)
        return []
    
    data = response.json()
    issues = data.get("issues", [])
    print(f"✅ Found {len(issues)} open issues in SonarCloud")
    return issues


def get_rule_details(rule_key: str) -> Optional[Dict]:
    """Fetch detailed information about a SonarCloud rule"""
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    
    params = {
        "key": rule_key
    }
    
    response = requests.get(
        f"{SONAR_URL}/rules/show",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.json().get("rule", {})
    return None


def get_issue_snippet(component_key: str, start_line: int, end_line: int) -> Optional[str]:
    """Fetch the source code snippet for the issue"""
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    
    # Fetch a few lines of context around the error
    params = {
        "key": component_key,
        "from": max(1, start_line - 2),
        "to": end_line + 2
    }
    
    response = requests.get(
        f"{SONAR_URL}/sources/lines",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        lines = data.get("sources", [])
        code_lines = []
        for line_info in lines:
            line_num = line_info.get("line")
            code = line_info.get("code", "")
            prefix = ">> " if start_line <= line_num <= end_line else "   "
            code_lines.append(f"{prefix}{line_num}: {code}")
        return "\n".join(code_lines)
    return None


def check_jira_issue_exists(sonar_issue_key: str) -> bool:
    """Check if Jira issue already exists for this SonarCloud issue"""
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    
    jql = f'project = {JIRA_PROJECT_KEY} AND summary ~ "{sonar_issue_key}"'
    
    params = {
        "jql": jql,
        "maxResults": 1
    }
    
    response = requests.get(
        f"{JIRA_URL}/rest/api/3/search",
        auth=auth,
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        return data.get("total", 0) > 0
    return False


def create_jira_issue(sonar_issue: Dict) -> Optional[str]:
    """Create a Jira issue from a SonarCloud issue"""
    
    # Check if issue already exists
    sonar_key = sonar_issue.get("key")
    # TEMPORARY DEBUG: Disable duplicate check to force creation
    # if check_jira_issue_exists(sonar_key):
    #     print(f"⏭️  Jira issue already exists for {sonar_key}, skipping...")
    #     return None
    
    # Get rule details
    rule_key = sonar_issue.get("rule")
    rule_details = get_rule_details(rule_key)
    
    # Get issue details
    severity = sonar_issue.get("severity", "UNKNOWN")
    message = sonar_issue.get("message", "No description")
    component_full = sonar_issue.get("component", "")
    component = component_full.split(":")[-1]
    
    text_range = sonar_issue.get("textRange", {})
    start_line = text_range.get("startLine", 0)
    end_line = text_range.get("endLine", 0)
    
    # Build issue description
    description_parts = [
        f"*SonarCloud Issue:* {sonar_key}",
        f"*Severity:* {severity}",
        f"*Rule:* {rule_key}",
        f"*File:* {component}",
        f"*Line:* {start_line}",
        "",
        f"*Message:* {message}",
        "",
    ]
    
    # Add Code Snippet
    if start_line > 0:
        code_snippet = get_issue_snippet(component_full, start_line, end_line)
        if code_snippet:
            description_parts.extend([
                "*Violating Code:*",
                "{code:python}",
                code_snippet,
                "{code}",
                ""
            ])
    
    if rule_details:
        description_parts.extend([
            f"*Rule Description:*",
            rule_details.get("htmlDesc", rule_details.get("mdDesc", "No description available")),
            "",
        ])
    
    # Add link to SonarCloud
    sonar_link = f"https://sonarcloud.io/project/issues?id={SONAR_PROJECT_KEY}&open={sonar_key}"
    description_parts.extend([
        f"*SonarCloud Link:*",
        sonar_link
    ])
    
    description = "\n".join(description_parts)
    
    # Prepare Jira issue payload
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    
    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"[SonarCloud] {message[:100]} ({sonar_key})",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": JIRA_ISSUE_TYPE
            }
        }
    }
    
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        auth=auth,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 201:
        jira_issue = response.json()
        jira_key = jira_issue.get("key")
        print(f"✅ Created Jira issue: {jira_key} for SonarCloud issue: {sonar_key}")
        return jira_key
    else:
        print(f"❌ Failed to create Jira issue for {sonar_key}: {response.status_code}")
        print(response.text)
        return None


def main():
    """Main execution function"""
    print("🚀 Starting SonarCloud to Jira Integration...")
    
    # Validate credentials
    if not SONAR_TOKEN:
        print("❌ SONAR_TOKEN not found in environment")
        sys.exit(1)
    
    if not JIRA_API_TOKEN or not JIRA_EMAIL:
        print("❌ JIRA_API_TOKEN or JIRA_EMAIL not found in environment")
        sys.exit(1)
    
    # Fetch SonarCloud issues
    sonar_issues = get_sonar_issues()
    
    if not sonar_issues:
        print("✅ No open issues found in SonarCloud via API.")
        print("💡 NOTE: If you just pushed code, SonarCloud might still be processing. Check the dashboard.")
        return
    
    # Create Jira issues
    created_count = 0
    for issue in sonar_issues:
        jira_key = create_jira_issue(issue)
        if jira_key:
            created_count += 1
    
    print(f"\n🎉 Integration complete!")
    print(f"📊 Created {created_count} new Jira issues out of {len(sonar_issues)} SonarCloud issues")


if __name__ == "__main__":
    main()
