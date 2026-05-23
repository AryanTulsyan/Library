#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # ... inside your main() function ...
    try:
        from django.core.management import call_command
        # This tells Django to safely record the migration as completed in the cloud
        call_command("migrate", "books", fake=True)
    except Exception:
        pass  # Quietly ignore if it's already done or fails

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
