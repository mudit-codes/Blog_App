# Deployment Guide

This guide covers deploying the Flask Blog App to various platforms.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

## Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/mudit-codes/Blog_App.git
   cd Blog_App
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key-here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Production Deployment

### Heroku

1. **Create a Heroku account** at https://heroku.com

2. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

3. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

### Docker

1. **Create a Dockerfile**
   ```dockerfile
   FROM python:3.12-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   ENV FLASK_ENV=production
   
   EXPOSE 5000
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Build and run**
   ```bash
   docker build -t flask-blog .
   docker run -p 5000:5000 -e SECRET_KEY=your-secret-key flask-blog
   ```

### Traditional Server (Linux)

1. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Set up application**
   ```bash
   cd /var/www/blog-app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Gunicorn service**
   Create `/etc/systemd/system/blog-app.service`:
   ```ini
   [Unit]
   Description=Flask Blog App
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/blog-app
   Environment="PATH=/var/www/blog-app/venv/bin"
   Environment="FLASK_ENV=production"
   Environment="SECRET_KEY=your-secret-key"
   ExecStart=/var/www/blog-app/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx**
   Create `/etc/nginx/sites-available/blog-app`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   
       location /static {
           alias /var/www/blog-app/static;
       }
   }
   ```

5. **Enable and start services**
   ```bash
   sudo systemctl enable blog-app
   sudo systemctl start blog-app
   sudo systemctl enable nginx
   sudo systemctl restart nginx
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Secret key for sessions | dev-secret-key |
| `DATABASE_URL` | Database connection URL | SQLite in instance/ |
| `PORT` | Port to run the application | 5000 |

## Database Migrations

When you make changes to models:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Security Checklist for Production

- [ ] Set a strong `SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS (SSL certificate)
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable monitoring and logging
- [ ] Use a production database (PostgreSQL recommended)
- [ ] Configure rate limiting
- [ ] Set up CORS if needed
- [ ] Review and update security headers

## Performance Optimization

1. **Use Redis for caching** (recommended for production)
   ```python
   CACHE_TYPE = 'RedisCache'
   CACHE_REDIS_URL = 'redis://localhost:6379/0'
   ```

2. **Use PostgreSQL** instead of SQLite for production
   ```python
   DATABASE_URL = 'postgresql://user:pass@localhost/dbname'
   ```

3. **Enable gzip compression** in Nginx configuration

4. **Set up CDN** for static files

## Monitoring

- Check application logs: `tail -f instance/logs/blog_app.log`
- Monitor system resources: `htop`
- Set up application monitoring (New Relic, DataDog, etc.)

## Troubleshooting

### Database locked error
Solution: Use PostgreSQL instead of SQLite for production

### Permission denied
Solution: Check file permissions and user ownership

### 502 Bad Gateway
Solution: Ensure Gunicorn is running and listening on correct port

## Support

For issues and questions, please open an issue on GitHub.
