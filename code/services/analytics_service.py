from lms.mongodb import get_analytics_collection
from datetime import datetime, timezone

def record_content_view(user_id, course_id, content_id=None):
    collection = get_analytics_collection()
    collection.insert_one({
        'user_id': user_id,
        'course_id': course_id,
        'content_id': content_id,
        'event_type': 'view',
        'timestamp': datetime.now(timezone.utc)
    })

def get_popular_courses(limit=5):
    collection = get_analytics_collection()
    pipeline = [
        {'$match': {'event_type': 'view'}},
        {'$group': {'_id': '$course_id', 'views': {'$sum': 1}}},
        {'$sort': {'views': -1}},
        {'$limit': limit}
    ]
    return list(collection.aggregate(pipeline))