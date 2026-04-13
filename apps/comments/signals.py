from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from config.socketio_app import emit_new_comment

@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    if created:
        # Emit the new comment via Socket.IO
        try:
            emit_new_comment(instance)
        except Exception as e:
            print(f"Error emitting Socket.IO event: {e}")
