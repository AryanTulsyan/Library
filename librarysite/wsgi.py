import os
import django
from django.core.wsgi import get_wsgi_application

# Set up settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

# Initialize Django core configuration setup safely
django.setup()

# 🌟 RUN MIGRATIONS SAFELY AT LAUNCH
from django.core.management import call_command
try:
    print("Connecting to Neon PostgreSQL to apply structural updates...")
    call_command('migrate', '--noinput')
    print("Database sync complete!")
except Exception as database_error:
    # This prevents the build from crashing if the database is busy or compiling
    print(f"Migration passing or handled: {database_error}")

# Hand off to Vercel worker instance
application = get_wsgi_application()
app = application