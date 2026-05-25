import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

# 🌟 FORCE MIGRATIONS ON VERCEL STARTUP
# This executes before the application fully launches, syncing Neon with your code
from django.core.management import call_command
try:
    print("Running production database migrations...")
    call_command('migrate', '--noinput')
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Migration failed or skipped: {e}")

application = get_wsgi_application()
app = application