from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from config.socketio_app import emit_new_notification
from apps.posts.models import Post
from apps.comments.models import Comment
from apps.accounts.models import User

@receiver(post_save, sender=Notification)
def notification_saved(sender, instance, created, **kwargs):
    if created:
        try:
            emit_new_notification(instance)
        except Exception as e:
            print(f"Error emitting Notification Socket.IO event: {e}")

@receiver(post_save, sender=Post)
def create_post_notifications(sender, instance, created, **kwargs):
    if created:
        if instance.post_type == 'GLOBAL':
            users = User.objects.filter(is_active=True).exclude(id=instance.author.id)
            notifications = [
                Notification(
                    user=user,
                    message=f"Nouvelle publication: {instance.title}",
                    notification_type='NEW_POST',
                    related_post=instance
                )
                for user in users
            ]
            Notification.objects.bulk_create(notifications)
            
            # Since bulk_create doesn't trigger post_save signals, we emit manually
            for notif in Notification.objects.filter(related_post=instance, notification_type='NEW_POST'):
                emit_new_notification(notif)
                
        elif instance.post_type == 'CLASS' and instance.classroom:
            # Get students in class
            users_to_notify = list(User.objects.filter(student_profile__classroom=instance.classroom, is_active=True).exclude(id=instance.author.id))
            # Get teachers for class
            teachers = User.objects.filter(teacher_profile__classrooms=instance.classroom, is_active=True).exclude(id=instance.author.id)
            users_to_notify.extend(list(teachers))
            
            notifications = [
                Notification(
                    user=user,
                    message=f"Nouvelle publication pour {instance.classroom.name}: {instance.title}",
                    notification_type='NEW_POST',
                    related_post=instance
                )
                for user in set(users_to_notify)
            ]
            Notification.objects.bulk_create(notifications)
            
            for notif in Notification.objects.filter(related_post=instance, notification_type='NEW_POST'):
                emit_new_notification(notif)
                
        elif instance.post_type == 'PERSONAL' and instance.target_user:
            if instance.target_user.id != instance.author.id:
                notif = Notification.objects.create(
                    user=instance.target_user,
                    message=f"Vous avez reçu une publication : {instance.title}",
                    notification_type='NEW_POST',
                    related_post=instance
                )
                # post_save of Notification will trigger emit_new_notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # Notify post author if they are not the commenter
        if instance.post.author.id != instance.author.id:
            Notification.objects.create(
                user=instance.post.author,
                message=f"{instance.author.username} a commenté votre publication : {instance.post.title}",
                notification_type='NEW_COMMENT',
                related_post=instance.post
            )
