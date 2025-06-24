# Heroku Deployment Checklist for Eevee Emporium

## Pre-Deployment Steps

1. **Environment Variables on Heroku:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set USE_AWS=True (if using S3)
   heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket
   heroku config:set AWS_ACCESS_KEY_ID=your-key
   heroku config:set AWS_SECRET_ACCESS_KEY=your-secret
   heroku config:set STRIPE_PUBLIC_KEY=your-stripe-public
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret
   ```

2. **Optional Redis (for better performance):**
   ```bash
   heroku addons:create heroku-redis:mini
   # This automatically sets REDIS_URL
   ```

## Key Changes Made

1. **Template Configuration**: Fixed APP_DIRS conflict with loaders
2. **Conditional Compressor**: Only loads in production to avoid dev issues
3. **Flexible Caching**: Falls back to database cache if Redis unavailable
4. **Better Procfile**: Includes all necessary setup commands
5. **Error Handling**: Graceful degradation for missing services

## Testing Deployment

Run these commands locally first:
```bash
# Test with production-like settings
export DEBUG=False
python manage.py check --deploy
python manage.py migrate --noinput
python manage.py setup_cache
python manage.py collectstatic --noinput
```

## Common Issues Fixed

- **Template Loader Conflict**: Fixed APP_DIRS vs custom loaders
- **Missing Static Files**: Added collectstatic to release process
- **Cache Dependency**: Made Redis optional with database fallback
- **Compressor Issues**: Only enabled in production

## If Deployment Still Fails

1. Check Heroku logs: `heroku logs --tail`
2. Disable performance features temporarily by commenting out:
   - Cache middleware in MIDDLEWARE
   - Compressor in INSTALLED_APPS
3. Use basic configuration for initial deployment
4. Re-enable features one by one
