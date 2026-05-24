import os
import sys

# Get the directory where this wsgi.py file lives (librarysite folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the root directory where manage.py lives
root_dir = os.path.dirname(current_dir)

# Tell Python to check both directories for your settings and modules
sys.path.append(current_dir)
sys.path.append(root_dir)

from django.core.wsgi import get_wsgi_application

# Point explicitly to the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

# Expose the application handlers to Vercel's builder
application = get_wsgi_application()
app = application