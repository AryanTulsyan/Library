import os
import sys

# Tell Python where to find your app packages
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')

# These MUST be defined at the absolute top-level of the file with no nesting
application = get_wsgi_application()
app = application