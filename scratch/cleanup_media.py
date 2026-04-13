import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.posts.models import PostMedia

def cleanup_missing_media():
    all_media = PostMedia.objects.all()
    missing_count = 0
    for m in all_media:
        try:
            if not os.path.exists(m.file.path):
                print(f"Missing file: {m.file.name} - Deleting reference.")
                m.delete()
                missing_count += 1
        except ValueError:
            # Handle cases where m.file is empty or invalid
            print(f"Invalid file reference for ID {m.id} - Deleting reference.")
            m.delete()
            missing_count += 1
            
    print(f"Cleanup complete. Removed {missing_count} missing media references.")

if __name__ == "__main__":
    cleanup_missing_media()
