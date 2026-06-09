# 🚀 Deployment Guide - Sugandhit Space

Complete guide to deploy the Sugandhit Space gardening app to production.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Configuration](#production-configuration)
5. [Database Migration](#database-migration)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation Steps

```bash
# 1. Clone repository
cd sugandhit-app

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Initialize database
python init_db.py

# 7. Run application
python app.py
```

Access at: **http://localhost:5000**

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose (optional)

### Simple Docker Setup

```bash
# Build image
docker build -t sugandhit-app .

# Run container
docker run -p 5000:5000 \
  -e RAZORPAY_KEY_ID=your_key \
  -e RAZORPAY_KEY_SECRET=your_secret \
  -v sugandhit_db:/app \
  sugandhit-app
```

### Docker Compose Setup

```bash
# Set environment variables
export RAZORPAY_KEY_ID=your_key
export RAZORPAY_KEY_SECRET=your_secret

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access at: **http://localhost**

---

## Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create sugandhit-app

# Add environment variables
heroku config:set RAZORPAY_KEY_ID=your_key
heroku config:set RAZORPAY_KEY_SECRET=your_secret
heroku config:set JWT_SECRET_KEY=your_secret

# Add Procfile (create if not exists)
echo "web: gunicorn --bind 0.0.0.0:\$PORT app:create_app()" > Procfile

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 20.04 LTS)

# 2. Connect to instance and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# 3. Clone repository
git clone <your-repo-url>
cd sugandhit-app

# 4. Setup Python environment
python3 -m venv venv
source venv/bin/activate

# 5. Install requirements
pip install -r requirements.txt
pip install gunicorn

# 6. Initialize database
python init_db.py

# 7. Create systemd service
sudo nano /etc/systemd/system/sugandhit.service
```

Add to service file:
```ini
[Unit]
Description=Sugandhit Space App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/sugandhit-app
Environment="PATH=/home/ubuntu/sugandhit-app/venv/bin"
ExecStart=/home/ubuntu/sugandhit-app/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:create_app()
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start sugandhit
sudo systemctl enable sugandhit

# Setup Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/sugandhit
```

### DigitalOcean App Platform

1. Fork repository to GitHub
2. Connect GitHub account to DigitalOcean
3. Create new App
4. Select GitHub repo
5. Configure environment variables
6. Deploy

---

## Production Configuration

### Security Settings

Update `config.py` for production:

```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
```

### Environment Variables

Create `.env` for production:

```bash
FLASK_ENV=production
FLASK_APP=app.py
JWT_SECRET_KEY=generate-secure-random-key
RAZORPAY_KEY_ID=production_key
RAZORPAY_KEY_SECRET=production_secret
DATABASE_URL=postgresql://user:pass@host:5432/sugandhit
```

### Database Migration to PostgreSQL

```bash
# Install PostgreSQL client
pip install psycopg2

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/sugandhit

# Run database initialization
python init_db.py
```

### SSL/HTTPS

Use Let's Encrypt with Certbot:

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d yourdomain.com

# Update Nginx config to use SSL
sudo nano /etc/nginx/sites-available/sugandhit
```

---

## Database Migration

### SQLite to PostgreSQL

```bash
# 1. Export SQLite data
python -c "
from app import create_app
from models import db
app = create_app('development')
with app.app_context():
    # Export data to JSON
    pass
"

# 2. Setup PostgreSQL database
createdb sugandhit

# 3. Update connection string
export DATABASE_URL=postgresql://user:password@localhost/sugandhit

# 4. Initialize tables
python init_db.py

# 5. Migrate data (use your migration script)
```

---

## Monitoring & Maintenance

### Application Monitoring

Use tools like:
- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **DataDog** - Infrastructure monitoring

Setup Sentry:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### Backup Strategy

```bash
# Backup database daily
0 2 * * * pg_dump sugandhit > /backups/sugandhit_$(date +\%Y\%m\%d).sql

# Backup to S3
0 3 * * * aws s3 cp /backups/ s3://my-bucket/backups/ --recursive
```

### Log Management

Setup centralized logging:
```python
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

### Performance Optimization

1. **Enable caching**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

2. **Optimize database queries**
   - Add indexes
   - Use eager loading
   - Optimize N+1 queries

3. **CDN for static files**
   - Serve static files from CDN
   - Compress images
   - Minimize CSS/JS

### Health Checks

Create health check endpoint:

```python
@app.route('/health')
def health():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
```

---

## Common Issues

### Database Connection Error
- Check `DATABASE_URL`
- Verify database server is running
- Check credentials and permissions

### High Memory Usage
- Check for memory leaks
- Optimize database queries
- Increase worker processes

### Slow Page Load
- Enable caching
- Optimize database queries
- Use CDN for assets
- Compress static files

---

## Performance Benchmarks

Target metrics:
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 500ms
- **Uptime**: > 99.9%
- **Error Rate**: < 0.1%

---

## Support & Troubleshooting

For issues:
1. Check application logs
2. Monitor error tracking (Sentry)
3. Review database performance
4. Check server resources (CPU, Memory)

---

For more help, see [README.md](README.md) or contact info@sugandhit.com
