import logging
from .models import AuditLog

logger = logging.getLogger('audit')

def log_admin_action(user, action, target, details="", ip_address=None):
    """Enregistre une action administrative dans la base de données et dans le fichier de log"""
    AuditLog.objects.create(
        user=user,
        action=action,
        target=target,
        details=details,
        ip_address=ip_address
    )
    logger.info(f"ADMIN ACTION: {user} | {action} | {target} | {details} | IP: {ip_address}")
