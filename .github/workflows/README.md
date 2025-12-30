# GitHub Actions Workflows

This directory contains CI/CD workflows for the QA Dashboard project.

## Workflows

### 1. `qa-tests.yml` - Automated QA Testing

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`
- Scheduled runs every 6 hours
- Manual trigger via GitHub UI

**What it does:**
- Sets up Python 3.11 environment
- Installs dependencies (`requests`)
- Runs `torture_test.py` against your n8n webhook
- Uploads test artifacts
- Sends notifications on failure

**Required Secrets:**
- `N8N_WEBHOOK_URL` - Your n8n webhook endpoint

### 2. `docker-build.yml` - Docker Image Build & Push

**Triggers:**
- Push to `main` branch
- Version tags (e.g., `v1.0.0`)
- Manual trigger

**What it does:**
- Builds the dashboard Docker image
- Pushes to GitHub Container Registry (ghcr.io)
- Tags images with version/SHA
- Uses build cache for faster builds

**No secrets required** - Uses automatic `GITHUB_TOKEN`

## Setup Instructions

### 1. Add Repository Secrets

Go to: **Settings → Secrets and variables → Actions → New repository secret**

Add:
```
Name: N8N_WEBHOOK_URL
Value: https://qaoneorigin.app.n8n.cloud/webhook/testairr
```

### 2. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"

### 3. Manual Trigger

To run tests manually:
1. Go to **Actions** tab
2. Select "QA Regression Tests"
3. Click "Run workflow"
4. Choose branch and click "Run workflow"

## Viewing Results

### Test Results
- Go to **Actions** tab
- Click on any workflow run
- View logs in the "Run QA Tests" step
- Download artifacts if available

### Docker Images
- View built images at: `https://github.com/YOUR_USERNAME/YOUR_REPO/pkgs/container/YOUR_REPO%2Fqa-dashboard`
- Pull images: `docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO/qa-dashboard:latest`

## Notifications

To add Slack/Discord notifications on test failures, update the `notify` job in `qa-tests.yml`:

**Slack Example:**
```yaml
- name: Send Slack notification
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "❌ QA Tests Failed!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "QA regression tests failed. <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View logs>"
            }
          }
        ]
      }
```

## Troubleshooting

### Tests fail with connection error
- Verify `N8N_WEBHOOK_URL` secret is set correctly
- Ensure n8n webhook is publicly accessible
- Check n8n service is running

### Docker build fails
- Check Dockerfile syntax in `dashboard-ui/Dockerfile`
- Verify `dashboard.html` exists in `dashboard-ui/`
- Review build logs for specific errors

### Scheduled runs not working
- Ensure repository is not archived
- Check that Actions are enabled
- Verify cron syntax is correct
