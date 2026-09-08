#!/usr/bin/env python3
"""Fallback: Create issues for repos that don't accept PRs"""
import os
from github import Github, GithubException
from utils import setup_logging, load_config, generate_entry

logger = setup_logging()

def create_issue(github_instance, target, site):
    """Create issue to suggest adding site"""
    try:
        repo = github_instance.get_repo(target['repo'])
        
        # Check existing
        query = f"repo:{target['repo']} {site['url']} in:title,body"
        existing = list(github_instance.search_issues(query, state='all'))
        if existing:
            logger.info(f"Already submitted to {target['repo']}, skipping")
            return False
        
        # Create issue
        issue_title = f"Suggestion: Add {site['name']}"
        issue_body = f"""## Resource Suggestion

{generate_entry(site)}

**Category:** {target['category']}

---
*This suggestion was created by an automated contribution tool.*
"""
        
        issue = repo.create_issue(
            title=issue_title,
            body=issue_body
        )
        
        logger.info(f"✓ Issue created: {issue.html_url}")
        return True
        
    except GithubException as e:
        logger.error(f"GitHub API error: {e}")
        return False

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    sites_config = load_config('SITES_CONFIG')
    targets_config = load_config('TARGETS_CONFIG')
    
    g = Github(github_token)
    
    for site in sites_config.get('sites', []):
        for target in targets_config.get('targets', []):
            create_issue(g, target, site)

if __name__ == "__main__":
    main()
