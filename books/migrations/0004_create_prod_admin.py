from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    # Only run this if we are connected to the cloud Neon DB
    if os.environ.get('DATABASE_URL'):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Change 'admin' and 'yourpassword123' to whatever credentials you want!
        username = 'admin'
        email = 'admin@example.com'
        password = 'yourpassword123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"🚀 Cloud Superuser '{username}' successfully created!")

class Migration(migrations.Migration):
    dependencies = [
        # This will automatically list your previous migration filename here. Keep it as is!
        ('books', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]