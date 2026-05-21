import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

application = get_wsgi_application()

# ---- ADD THIS AUTO-MIGRATE BLOCK HERE ----
if os.environ.get('DATABASE_URL'):
    try:
        from django.core.management import call_command
        print("Running production migrations via WSGI boot...")
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration on boot failed: {e}")