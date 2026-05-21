import os
import sys
import traceback

print("--- DIAGNOSTIC START ---")
try:
    import django
    print("Django package imported successfully.")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librarysite.settings')
    django.setup()
    print("Django setup completed successfully.")
    
    from django.db import connection
    print("Attempting database connection...")
    connection.ensure_connection()
    print("Database connection verified successfully!")
    
except Exception as e:
    print("\n!!! CRASH DETECTED !!!")
    traceback.print_exc()
    sys.exit(1)

print("--- DIAGNOSTIC END ---")