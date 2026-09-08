# Web Resource Contributor

Automated GitHub PR/Issue submission for web resources to curated lists.

## Features

- Daily automated submissions via GitHub Actions
- Multi-site support with encrypted config
- Smart PR creation with proper formatting
- Issue fallback for non-PR repos
- Rate limit handling

## Setup

1. Fork this repo
2. Add GitHub Secrets:
   - `GITHUB_TOKEN`: Personal Access Token (scope: `public_repo`)
   - `SITES_CONFIG`: JSON with site details
   - `TARGETS_CONFIG`: JSON with target repositories
3. Enable Actions in repo settings
4. Workflow runs daily at 02:00 UTC

## Configuration

See `config/targets_template.yaml` for examples.

## Sites Config Example

```json
{
  "sites": [{
    "name": "mysite",
    "url": "https://mysite.com",
    "description": "Short tagline here",
    "features": ["Feature 1", "Feature 2"],
    "tags": ["tag1", "tag2"]
  }]
}
```

## License

MIT
