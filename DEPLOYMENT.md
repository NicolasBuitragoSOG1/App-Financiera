# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Quick Start
1. Run `setup.bat` to install dependencies and initialize the database
2. Configure your OpenAI API key in `backend/.env`
3. Run `start.bat` to launch both servers
4. Access the application at http://localhost:3000

### Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_data.py
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Docker Deployment

### Using Docker Compose
```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Container Builds
```bash
# Build backend
docker build -t finance-backend ./backend

# Build frontend
docker build -t finance-frontend ./frontend

# Run with custom network
docker network create finance-network
docker run -d --name finance-db --network finance-network postgres:15
docker run -d --name finance-backend --network finance-network finance-backend
docker run -d --name finance-frontend --network finance-network -p 3000:3000 finance-frontend
```

## Production Deployment

### Environment Variables
Create a `.env.production` file:
```
SECRET_KEY=your-very-long-and-secure-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=https://yourdomain.com
```

### Database Migration
```bash
# For production, use PostgreSQL
pip install psycopg2-binary
python -c "from database import create_tables; create_tables()"
python init_data.py
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL/HTTPS Setup
```bash
# Using Certbot
sudo certbot --nginx -d yourdomain.com
```

## Cloud Deployment Options

### AWS
- Use ECS or EKS for container orchestration
- RDS for PostgreSQL database
- CloudFront for CDN
- Route 53 for DNS

### Google Cloud
- Use Cloud Run for serverless containers
- Cloud SQL for PostgreSQL
- Cloud CDN for static assets

### Azure
- Use Container Instances or AKS
- Azure Database for PostgreSQL
- Azure CDN

## Monitoring and Logging

### Application Monitoring
```python
# Add to main.py
import logging
logging.basicConfig(level=logging.INFO)

# Health check endpoint already included
GET /api/health
```

### Database Monitoring
```sql
-- Monitor database performance
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_database;
```

## Backup Strategy

### Database Backup
```bash
# PostgreSQL backup
pg_dump -h localhost -U finance_user finance_db > backup.sql

# Restore
psql -h localhost -U finance_user finance_db < backup.sql
```

### Automated Backups
```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Database**: Use strong passwords and connection encryption
3. **HTTPS**: Always use SSL/TLS in production
4. **CORS**: Configure appropriate CORS origins
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Input Validation**: All inputs are validated on both client and server
7. **Authentication**: JWT tokens with proper expiration

## Performance Optimization

1. **Database Indexing**: Key fields are indexed
2. **Caching**: Implement Redis for session caching
3. **CDN**: Use CDN for static assets
4. **Compression**: Gzip compression enabled
5. **Lazy Loading**: Frontend components are lazy-loaded

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in configuration files
2. **Database connection**: Check DATABASE_URL and credentials
3. **CORS errors**: Verify CORS_ORIGINS configuration
4. **API key errors**: Ensure OPENAI_API_KEY is set correctly

### Debug Mode
```bash
# Backend debug
uvicorn main:app --reload --log-level debug

# Frontend debug
npm run dev -- --debug
```
