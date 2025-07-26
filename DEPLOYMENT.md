# Deployment Guide for Tritiq ERP Web Application

## Overview
This guide covers deploying the Tritiq ERP web application to various platforms, with a focus on Supabase for the database and cloud platforms for the application.

## Prerequisites
- Completed local development setup
- Git repository access
- Database backup (if migrating existing data)

## Database Setup (Supabase)

### 1. Create Supabase Project
1. Visit [Supabase](https://supabase.com) and create an account
2. Create a new project
3. Choose your region and set a strong database password
4. Wait for project initialization (2-3 minutes)

### 2. Get Database Connection String
1. Go to Project Settings → Database
2. Copy the connection string under "Connection parameters"
3. Replace `[YOUR-PASSWORD]` with your actual password

Example connection string:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xyz.supabase.co:5432/postgres
```

### 3. Configure Environment Variables
Update your `.env` file for production:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.xyz.supabase.co:5432/postgres
ENVIRONMENT=production
SECRET_KEY=your-very-strong-secret-key-here
DEBUG=False
```

### 4. Run Database Migrations
```bash
# Ensure you're in the project root
alembic upgrade head
```

## Application Deployment Options

### Option 1: Railway (Recommended)

Railway provides easy deployment with PostgreSQL support:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**
   ```bash
   railway login
   railway init
   railway add --service postgresql
   railway deploy
   ```

3. **Set Environment Variables**
   ```bash
   railway variables:set DATABASE_URL="your_supabase_connection_string"
   railway variables:set SECRET_KEY="your_secret_key"
   railway variables:set ENVIRONMENT="production"
   ```

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create tritiq-erp-web
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set DATABASE_URL="your_supabase_connection_string"
   heroku config:set SECRET_KEY="your_secret_key"
   heroku config:set ENVIRONMENT="production"
   ```

4. **Create Procfile**
   ```bash
   echo "web: uvicorn src.main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

### Option 3: Vercel (Serverless)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create vercel.json**
   ```json
   {
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Set Environment Variables in Vercel Dashboard**
   - Go to your project in Vercel dashboard
   - Navigate to Settings → Environment Variables
   - Add all required environment variables

### Option 4: DigitalOcean App Platform

1. **Connect Repository**
   - Go to DigitalOcean App Platform
   - Create new app from GitHub repository

2. **Configure Build Settings**
   - Build Command: `pip install -r src/requirements.txt`
   - Run Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - Add all required environment variables in the app settings

## Production Configuration

### Security Considerations

1. **Strong Secret Key**
   ```python
   import secrets
   SECRET_KEY = secrets.token_urlsafe(32)
   ```

2. **CORS Configuration**
   ```python
   ALLOWED_ORIGINS = ["https://yourdomain.com"]
   ```

3. **Database Connection Pooling**
   ```python
   # In production, consider connection limits
   engine = create_async_engine(
       DATABASE_URL,
       pool_size=5,
       max_overflow=10,
       pool_timeout=30
   )
   ```

### Performance Optimization

1. **Static Files**
   - Use a CDN for static files in production
   - Configure proper caching headers

2. **Database Optimization**
   - Enable connection pooling
   - Use database indexes for frequently queried fields
   - Regular database maintenance

3. **Monitoring**
   - Set up application monitoring (Sentry, LogRocket)
   - Database performance monitoring
   - Uptime monitoring

## Data Migration

### From Desktop Application

If migrating from the PySide6 desktop application:

1. **Export Data from Desktop App**
   - Use the backup functionality in the desktop app
   - Export to JSON or CSV format

2. **Create Migration Script**
   ```python
   # src/scripts/migrate_desktop_data.py
   import json
   from src.db.session import get_db_context
   from src.db.crud import users, companies, products  # etc.
   
   async def migrate_data():
       with open('desktop_backup.json', 'r') as f:
           data = json.load(f)
       
       async with get_db_context() as db:
           # Migrate users, companies, products, etc.
           pass
   ```

3. **Run Migration**
   ```bash
   python -c "import asyncio; from src.scripts.migrate_desktop_data import migrate_data; asyncio.run(migrate_data())"
   ```

## SSL/HTTPS Setup

### Using Cloudflare (Recommended)

1. Add your domain to Cloudflare
2. Update nameservers
3. Enable "Always Use HTTPS"
4. Set SSL/TLS mode to "Full (strict)"

### Using Let's Encrypt

For VPS deployments:
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Maintenance

### Log Management
```python
# Configure structured logging
import structlog

logger = structlog.get_logger()
```

### Database Backups
```bash
# Automated daily backups
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Health Checks
```python
# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify connection string format
   - Check firewall settings
   - Ensure database is accessible from deployment platform

2. **Static Files Not Loading**
   - Verify static file configuration
   - Check file paths and permissions
   - Use absolute URLs for static files

3. **Memory Issues**
   - Monitor application memory usage
   - Optimize database queries
   - Consider connection pooling

### Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Review platform-specific documentation

## Cost Optimization

### Supabase
- Free tier: 500MB database, 2GB bandwidth
- Pro tier: $25/month for production use

### Application Hosting
- Railway: ~$5-20/month depending on usage
- Heroku: $7/month for basic dyno
- Vercel: Free for hobby projects, $20/month for teams
- DigitalOcean: $5-25/month depending on resources

Choose based on your traffic expectations and budget requirements.