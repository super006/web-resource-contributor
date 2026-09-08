import json
import os
import logging
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "submission.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config(env_var):
    """Load JSON config from environment variable"""
    config_str = os.getenv(env_var)
    if not config_str:
        raise ValueError(f"Missing environment variable: {env_var}")
    return json.loads(config_str)

def format_features(features):
    """Format feature list for markdown"""
    if not features:
        return ""
    return "\n".join([f"- {f}" for f in features])

def format_tags(tags):
    """Format tags for markdown"""
    if not tags:
        return ""
    return " ".join([f"`{t}`" for t in tags])

def generate_entry(site):
    """Generate markdown entry for a site"""
    entry = f"### [{site['name']}]({site['url']})\n\n"
    entry += f"{site['description']}\n\n"
    
    if site.get('features'):
        entry += "**Features:**\n"
        entry += format_features(site['features']) + "\n\n"
    
    if site.get('tags'):
        entry += f"**Tags:** {format_tags(site['tags'])}\n\n"
    
    return entry

def check_rate_limit(github_instance):
    """Check GitHub API rate limit"""
    rate_limit = github_instance.get_rate_limit()
    remaining = rate_limit.core.remaining
    
    if remaining < 10:
        return False, f"Rate limit low: {remaining} requests remaining"
    
    return True, f"Rate limit OK: {remaining} requests remaining"
