# QA Dashboard - Production Deployment

A Dockerized QA regression testing dashboard with n8n workflow automation for the Airr 3.0 pipeline.

## 🏗️ Architecture

This stack consists of two services:

1. **qa-dashboard** - React-based dashboard served via nginx
   - Displays real-time QA test results from Supabase
   - Auto-refreshes every 5 seconds
   - Beautiful UI with pass/fail statistics

2. **n8n** - Workflow automation platform
   - Handles webhook endpoints for test execution
   - Manages data validation workflows
   - Persists workflows in Docker volume

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Supabase account with `qa_runs` table configured
- GitHub account (for CI/CD automation)

## 🚀 Quick Start

### 1. Deploy the Stack

```bash
docker-compose up -d
```

This will:
- Build the dashboard from `./dashboard-ui`
- Pull the n8n image
- Start both services in detached mode
- Create persistent volume for n8n data

### 2. Access the Services

- **QA Dashboard**: http://localhost:3000
- **n8n Workflow Editor**: http://localhost:5678

### 3. Configure n8n Webhooks

1. Open n8n at http://localhost:5678
2. Create your validation workflow
3. Set up webhook nodes to receive test data
4. Update `torture_test.py` with the webhook URL

## 📁 Project Structure

```
.
├── dashboard-ui/
│   ├── dashboard.html      # React dashboard (single-file)
│   └── Dockerfile          # nginx-alpine container
├── docker-compose.yml      # Orchestration file
├── torture_test.py         # Python test runner
└── README.md              # This file
```

## 🔧 Configuration

### Dashboard Configuration

Edit `dashboard-ui/dashboard.html` to update:
- Supabase URL and API key (lines 17-18)
- Auto-refresh interval (line 30, default: 5000ms)
- Display limit (line 34, default: 50 runs)

### n8n Configuration

Environment variables in `docker-compose.yml`:
- `N8N_SECURE_COOKIE=false` - Disable for local/testing (set to `true` in production with HTTPS)

## 🛠️ Management Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f qa-dashboard
docker-compose logs -f n8n
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Dashboard
```bash
docker-compose up -d --build qa-dashboard
```

### Reset n8n Data
```bash
docker-compose down -v
docker-compose up -d
```

## 🤖 GitHub Actions CI/CD

This project includes automated workflows for continuous testing and deployment.

### Available Workflows

#### 1. QA Regression Tests (`qa-tests.yml`)

Automatically runs your test suite on:
- Every push to `main` or `develop`
- Pull requests to `main`
- Scheduled runs every 6 hours
- Manual trigger via GitHub UI

**Setup:**
1. Go to **Settings → Secrets and variables → Actions**
2. Add secret: `N8N_WEBHOOK_URL` = `https://qaoneorigin.app.n8n.cloud/webhook/testairr`
3. Push code to trigger workflow

**Manual Run:**
```bash
# Via GitHub UI
Actions → QA Regression Tests → Run workflow

# Or trigger via API
gh workflow run qa-tests.yml
```

#### 2. Docker Build & Push (`docker-build.yml`)

Builds and publishes Docker images to GitHub Container Registry:
- Triggered on push to `main` or version tags
- Images available at: `ghcr.io/YOUR_USERNAME/YOUR_REPO/qa-dashboard`
- Automatic versioning and caching

**Pull the image:**
```bash
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO/qa-dashboard:latest
```

### Viewing Test Results

1. Go to **Actions** tab in your repository
2. Click on any workflow run
3. View detailed logs and download artifacts
4. Check test pass/fail status

### Adding Notifications

Edit `.github/workflows/qa-tests.yml` to add Slack/Discord alerts on test failures. See `.github/workflows/README.md` for examples.

## 🌐 Coolify Deployment

### Method 1: Docker Compose (Recommended)

1. Create a new service in Coolify
2. Select "Docker Compose" as the build pack
3. Point to your Git repository
4. Coolify will automatically detect `docker-compose.yml`
5. Set environment variables if needed
6. Deploy

### Method 2: Dockerfile

1. Create two separate services in Coolify
2. For the dashboard:
   - Build pack: Dockerfile
   - Dockerfile location: `./dashboard-ui/Dockerfile`
   - Port: 80
3. For n8n:
   - Build pack: Docker Image
   - Image: `n8nio/n8n`
   - Port: 5678

## 🔐 Production Considerations

1. **Supabase Keys**: Use environment variables instead of hardcoding
2. **n8n Security**: 
   - Set `N8N_SECURE_COOKIE=true`
   - Enable authentication
   - Use HTTPS/SSL
3. **CORS**: Configure Supabase CORS settings for your domain
4. **Monitoring**: Add health checks and logging

## 📊 Dashboard Features

- ✅ Real-time test result monitoring
- 📈 Pass/fail rate statistics
- 🔍 Detailed error breakdowns with field-level diffs
- 🎨 Modern UI with TailwindCSS
- ⚡ Auto-refresh every 5 seconds

## 🐛 Troubleshooting

### Dashboard shows "Invalid Error Format"
- Check that `error_log` in Supabase is valid JSON
- Verify the error structure matches: `{"error": "...", "field": "..."}`

### n8n workflows not persisting
- Ensure the `n8n_data` volume is created: `docker volume ls`
- Check volume permissions

### Connection errors in torture_test.py
- Verify n8n is running: `docker-compose ps`
- Check webhook URL matches n8n endpoint
- Ensure n8n container is accessible from host

## 📝 License

Internal QA Tool - Airr 3.0 Project
