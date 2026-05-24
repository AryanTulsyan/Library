import os
import sys

# Ensure the root directory is in Python's search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

try:
    application = get_wsgi_application()
    app = application
except Exception as e:
    # This prevents Vercel from failing to initialize the module completely
    print(f"WSGI initialization failed: {e}")
    raise e