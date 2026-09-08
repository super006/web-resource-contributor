#!/usr/bin/env python3
import os
import time
from github import Github, GithubException
from utils import (
    setup_logging,
    load_config,
    generate_entry,
    check_rate_limit
)

logger = setup_logging()

def find_insertion_point(content, category):
    """Find appropriate insertion point in README"""
    lines = content.split('\n')
    
    # Look for category header
    for i, line in enumerate(lines):
        if category.lower() in line.lower():
            # Find next list item or empty line
            for j in range(i, len(lines)):
                if lines[j].startswith('- ') or lines[j].startswith('* '):
                    return j
                if lines[j].strip() == '':
                    return j + 1
    
    # Fallback: add to end
    return len(lines)

def create_pr(github_instance, target, site):
    """Create PR to add site to target repository"""
    try:
        repo = github_instance.get_repo(target['repo'])
        logger.info(f"Processing repo: {target['repo']}")
        
        # Check if already submitted (search issues/PRs)
        query = f"repo:{target['repo']} {site['url']} in:title,body"
        existing = list(github_instance.search_issues(query, state='all'))
        if existing:
            logger.info(f"Already submitted to {target['repo']}, skipping")
            return False
        
        # Fork repo
        fork = github_instance.get_user().create_fork(repo)
        logger.info(f"Forked to {fork.full_name}")
        time.sleep(2)  # Wait for fork to be ready
        
        # Get README
        try:
            readme = fork.get_readme()
        except:
            logger.warning(f"No README found in {target['repo']}")
            return False
        
        # Prepare new content
        original_content = readme.decoded_content.decode('utf-8')
        entry = generate_entry(site)
        
        # Find insertion point
        insertion_line = find_insertion_point(original_content, target['category'])
        lines = original_content.split('\n')
        lines.insert(insertion_line, entry)
        new_content = '\n'.join(lines)
        
        # Create branch
        branch_name = f"add-{site['name']}-{int(time.time())}"
        source_branch = repo.get_branch(repo.default_branch)
        fork.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=source_branch.commit.sha
        )
        
        # Update README
        fork.update_file(
            path=readme.path,
            message=f"Add {site['name']} to {target['category']}",
            content=new_content,
            sha=readme.sha,
            branch=branch_name
        )
        
        # Create PR
        pr_title = f"Add {site['name']} - {site['description'][:50]}"
        pr_body = f"""## Add {site['name']}

{site['description']}

**URL:** {site['url']}

"""
        if site.get('features'):
            pr_body += "**Features:**\n"
            for feature in site['features']:
                pr_body += f"- {feature}\n"
        
        pr_body += "\n---\n*This PR was created by an automated contribution tool.*"
        
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=f"{fork.owner.login}:{branch_name}",
            base=repo.default_branch
        )
        
        logger.info(f"✓ PR created: {pr.html_url}")
        return True
        
    except GithubException as e:
        logger.error(f"GitHub API error for {target['repo']}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error processing {target['repo']}: {e}")
        return False

def main():
    logger.info("Starting submission workflow")
    
    # Load configs
    try:
        sites_config = load_config('SITES_CONFIG')
        targets_config = load_config('TARGETS_CONFIG')
        github_token = os.getenv('GITHUB_TOKEN')
        
        if not github_token:
            raise ValueError("Missing GITHUB_TOKEN")
            
    except Exception as e:
        logger.error(f"Config error: {e}")
        return
    
    # Initialize GitHub client
    g = Github(github_token)
    
    # Check rate limit
    ok, msg = check_rate_limit(g)
    logger.info(msg)
    if not ok:
        logger.error("Rate limit too low, aborting")
        return
    
    # Process each site
    for site in sites_config.get('sites', []):
        logger.info(f"\n=== Processing site: {site['name']} ===")
        
        # Sort targets by priority
        targets = sorted(
            targets_config.get('targets', []),
            key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x.get('priority', 'low'), 2)
        )
        
        success_count = 0
        for target in targets:
            if success_count >= 3:  # Limit to 3 PRs per run
                logger.info("Daily limit reached (3 PRs), stopping")
                break
                
            if create_pr(g, target, site):
                success_count += 1
                time.sleep(5)  # Rate limit courtesy
        
        logger.info(f"Submitted {success_count} PRs for {site['name']}")
    
    logger.info("\n=== Workflow complete ===")

if __name__ == "__main__":
    main()
