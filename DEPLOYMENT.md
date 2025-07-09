# Deployment Guide

This guide covers deploying VLSI Hero to various platforms.

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/vlsi_hero

# Flask Configuration
SESSION_SECRET=your-secret-key-here
FLASK_ENV=production

# Optional: Custom Port
PORT=5000
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

2. Set up PostgreSQL database
3. Set environment variables
4. Build CSS:
```bash
npm run build:css
```

5. Run the application:
```bash
python main.py
```

## Production Deployment

### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Using Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

2. Build and run:
```bash
docker build -t vlsi-hero .
docker run -p 5000:5000 vlsi-hero
```

### Heroku Deployment

1. Create `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Railway Deployment

1. Connect GitHub repository
2. Add PostgreSQL addon
3. Set environment variables
4. Deploy automatically

## Database Migration

For production deployments, use database migrations:

```python
from app import app, db
from models import User, Progress, Achievement, QuizAttempt, LearningSession, CircuitDesign

with app.app_context():
    db.create_all()
```

## Performance Optimization

### Database
- Use connection pooling
- Add database indexes for frequently queried fields
- Implement caching for static data

### Frontend
- Minify CSS and JavaScript
- Use CDN for static assets
- Implement lazy loading

### Server
- Use reverse proxy (Nginx)
- Enable gzip compression
- Set up SSL/TLS certificates

## Monitoring

### Health Checks
Add health check endpoint:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Logging
Configure proper logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Security

- Use HTTPS in production
- Set secure session cookies
- Implement rate limiting
- Regular security updates
- Database connection security

## Backup Strategy

- Regular database backups
- User data export functionality
- Version control for code
- Asset backup procedures