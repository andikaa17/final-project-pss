from datetime import datetime, timezone
from lms.mongodb import get_activity_collection
import logging

logger = logging.getLogger(__name__)

def log_activity(user_id, action, resource_type, resource_id, details=None, ip=None):
    """Log aktivitas user ke MongoDB"""
    try:
        collection = get_activity_collection()
        result = collection.insert_one({
            'user_id': user_id,
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'details': details or {},
            'ip_address': ip,
            'timestamp': datetime.now(timezone.utc)
        })
        logger.debug(f"Activity logged: {action} (id: {result.inserted_id})")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Failed to log activity: {e}")
        return None

def get_user_activities(user_id, limit=50):
    """Ambil riwayat aktivitas user"""
    collection = get_activity_collection()
    return list(collection.find({'user_id': user_id}).sort('timestamp', -1).limit(limit))

def get_course_activities(course_id, limit=50):
    """Ambil aktivitas terkait course"""
    collection = get_activity_collection()
    return list(collection.find({'resource_id': course_id}).sort('timestamp', -1).limit(limit))

def get_recent_activities(limit=100):
    """Ambil aktivitas terbaru"""
    collection = get_activity_collection()
    return list(collection.find().sort('timestamp', -1).limit(limit))